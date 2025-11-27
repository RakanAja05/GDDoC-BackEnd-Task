from .api.routes.api import router as api_router
from .api.routes.ui import router as ui_router
from .core.config import API_PREFIX, DEBUG, MEMOIZATION_FLAG, PROJECT_NAME, VERSION
from .core.events import create_start_app_handler
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    # Mount static assets
    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    # Include UI router at root (landing page)
    application.include_router(ui_router)
    application.include_router(api_router, prefix=API_PREFIX)
    application.add_event_handler("startup", create_start_app_handler(application))
    return application


app = get_application()
