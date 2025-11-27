from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from ...services.gemini_chat import gemini_chat
from ...services.personas import get_preset
from ...services.conversations import create_conversation, get_conversation_messages, append_message

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    system: Optional[str] = None
    user_profile: Optional[Dict[str, Any]] = None
    conversation: Optional[List[Dict[str, str]]] = None
    conversation_token: Optional[str] = None
    as_persona: Optional[bool] = False
    persona_preset: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    conversation_token: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest = Body(...)):
    """Endpoint to proxy a question to Gemini chat with optional user profile and system prompt."""
    if not gemini_chat.is_available():
        return {"reply": "Chat unavailable (Gemini API key not configured)."}

    user_profile = payload.user_profile or {}
    if payload.as_persona and payload.persona_preset:
        preset = get_preset(payload.persona_preset)
        merged = {**preset, **{k: v for k, v in (user_profile or {}).items() if v is not None}}
        user_profile = merged

    system_prompt = payload.system
    if payload.as_persona:
        name = user_profile.get("name") or "Saya"
        role = user_profile.get("role") or ""
        background = user_profile.get("background", "")
        prefs = user_profile.get("preference", "ringkas, first-person")
        tone = user_profile.get("tone", "santai, langsung")
        style_hint = user_profile.get("style_hint", "jawab singkat dan santai; gunakan kata 'saya' untuk merujuk pada diri sendiri.")

        parts = [
            f"You are roleplaying as {name}.",
            "Answer in Indonesian, in first-person (saya).",
            f"Role: {role}." if role else None,
            f"Tone: {tone}.",
            f"Style hint: {style_hint}.",
        ]
        if background:
            parts.append(f"Background: {background}.")
        if prefs:
            parts.append(f"Preferences: {prefs}.")

        parts.append("If you do not know something, say 'Saya tidak tahu' rather than inventing facts. Keep answers concise unless asked for more details.")

        system_prompt = " ".join([p for p in parts if p])

    conv_token = payload.conversation_token
    history = payload.conversation or []
    if conv_token:
        history = get_conversation_messages(conv_token)

    if conv_token:
        append_message(conv_token, 'user', payload.question)

    result = gemini_chat.chat(
        question=payload.question,
        user_profile=user_profile,
        system_prompt=system_prompt,
        conversation=history,
    )

    reply_text = result.get("reply", "")

    if conv_token:
        append_message(conv_token, 'assistant', reply_text)
    return {"reply": reply_text, "conversation_token": conv_token}



class ConversationCreateResponse(BaseModel):
    token: str


@router.post("/conversations", response_model=ConversationCreateResponse)
async def create_conversation_endpoint():
    token = create_conversation()
    return {"token": token}


@router.get("/conversations/{token}")
async def get_conversation_endpoint(token: str):
    msgs = get_conversation_messages(token)
    if msgs is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"messages": msgs}
