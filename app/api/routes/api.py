from fastapi import APIRouter

from . import predictor, menu, chat

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
router.include_router(menu.router, tags=["menu"])
router.include_router(chat.router, tags=["chat"]) 
