from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    # --- PERBAIKAN: Ganti 'metadata' menjadi 'extra_data' atau sejenisnya ---
    extra_data = Column(Text, nullable=True) 
    # ------------------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(32), nullable=False) 
    content = Column(Text, nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

    def __init__(self, conversation_id: int, role: str, content: str, created_at: datetime = None):
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        if created_at is not None:
            self.created_at = created_at