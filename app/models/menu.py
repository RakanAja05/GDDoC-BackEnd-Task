from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from pydantic import BaseModel, Field, ConfigDict
from ..db import Base


# SQLAlchemy Model
class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    calories = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    ingredients = Column(JSON, nullable=True)  # Stored as JSON array
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Pydantic Schemas
class MenuBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    calories: float = Field(..., ge=0)
    price: float = Field(..., ge=0)
    ingredients: Optional[List[str]] = Field(default_factory=list)
    description: Optional[str] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class MenuResponse(MenuBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuListResponse(BaseModel):
    data: List[MenuResponse]
    pagination: Optional[dict] = None


class MenuCreateResponse(BaseModel):
    message: str
    data: MenuResponse


class MenuUpdateResponse(BaseModel):
    message: str
    data: MenuResponse


class MenuDeleteResponse(BaseModel):
    message: str


class MenuGroupByCategoryCount(BaseModel):
    data: dict


class MenuGroupByCategoryList(BaseModel):
    data: dict
