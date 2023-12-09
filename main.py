from fastapi import FastAPI
from config.api_info import ProjectInfo
from registration.routes import agent_registration_router
from sync.routes import sync_device_info_router


def include_routers(app):
    app.include_router(agent_registration_router)
    app.include_router(sync_device_info_router)

def start_api():
    app = FastAPI(title=ProjectInfo.PROJECT_NAME, version=ProjectInfo.PROJECT_VERSION)
    include_routers(app)
    return app

app = start_api()