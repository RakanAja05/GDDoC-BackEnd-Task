from typing import List, Dict, Any, Optional
from uuid import uuid4
import json

from ..db import SessionLocal, engine, Base
from ..models.conversation import Conversation, ConversationMessage


def _ensure_tables():
    # create tables if they don't exist (safe for development)
    Base.metadata.create_all(bind=engine)


def create_conversation(metadata: Optional[Dict[str, Any]] = None) -> str:
    _ensure_tables()
    token = uuid4().hex
    db = SessionLocal()
    try:
        conv = Conversation(token=token, metadata=json.dumps(metadata or {}))
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return token
    finally:
        db.close()


def get_conversation_messages(token: str) -> List[Dict[str, Any]]:
    _ensure_tables()
    db = SessionLocal()
    try:
        conv = db.query(Conversation).filter(Conversation.token == token).first()
        if not conv:
            return []
        msgs = [
            {"role": m.role, "content": m.content, "created_at": m.created_at.isoformat()}
            for m in sorted(conv.messages, key=lambda x: x.id)
        ]
        return msgs
    finally:
        db.close()


def append_message(token: str, role: str, content: str) -> None:
    _ensure_tables()
    db = SessionLocal()
    try:
        conv = db.query(Conversation).filter(Conversation.token == token).first()
        if not conv:
            # create new conversation if not found
            conv = Conversation(token=token, extra_data=json.dumps({})) 
            db.add(conv)
            db.commit()
            db.refresh(conv)

      
        msg = ConversationMessage(conversation_id=conv.id, role=role, content=content)
        db.add(msg)
        db.commit()
    finally:
        db.close()
