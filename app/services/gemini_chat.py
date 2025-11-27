"""
Gemini Chat service

Provides a small wrapper to call Gemini for single-turn or multi-turn chat.
"""
from typing import Optional, List, Dict, Any
from loguru import logger
import google.generativeai as genai
from ..core.config import GEMINI_API_KEY


class GeminiChatService:
    """Simple Gemini chat wrapper."""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            try:
                # pick a model supported for generate_content
                # use the flash model consistent with other services
                self.model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception:
                logger.exception("Failed to initialize Gemini model")
                self.model = None
        else:
            self.model = None
            logger.warning("Gemini API key not configured for chat service")

    def is_available(self) -> bool:
        return self.model is not None

    def _sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        t = text.strip()
        if t.startswith("```"):
            # remove markdown fence
            parts = t.split("```")
            if len(parts) >= 2:
                t = parts[1]
        return t

    def chat(self, question: str, user_profile: Optional[Dict[str, Any]] = None, system_prompt: Optional[str] = None, conversation: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Perform a chat call to Gemini.

        - `question`: user question string
        - `user_profile`: optional dict with user info (will be included in prompt)
        - `system_prompt`: optional system instructions
        - `conversation`: optional list of previous turns: [{'role':'user'|'assistant','content':str}, ...]

        Returns dict: { 'reply': str, 'raw': optional raw response }
        """
        if not self.is_available():
            return {"reply": "Chat unavailable (Gemini API key not configured)."}

        # Build prompt
        pieces: List[str] = []
        if system_prompt:
            pieces.append(f"SYSTEM INSTRUCTIONS:\n{system_prompt}\n")

        if user_profile:
            # include small user summary
            try:
                profile_lines = []
                for k, v in user_profile.items():
                    profile_lines.append(f"- {k}: {v}")
                pieces.append("USER PROFILE:\n" + "\n".join(profile_lines) + "\n")
            except Exception:
                logger.exception("Failed to serialize user_profile for prompt")

        if conversation:
            for turn in conversation:
                role = turn.get("role", "user")
                content = turn.get("content", "")
                pieces.append(f"{role.upper()}: {content}\n")

        pieces.append(f"USER: {question}\nASSISTANT:")
        prompt = "\n".join(pieces)

        try:
            response = self.model.generate_content(prompt)
            text = self._sanitize_text(response.text or "")
            return {"reply": text, "raw": response}
        except Exception as e:
            logger.exception("Gemini chat call failed: %s", e)
            return {"reply": "Terjadi kesalahan saat menghubungi model."}


# singleton
gemini_chat = GeminiChatService()
