from fastapi import FastAPI

from api.routers.baska_bisi import router_2
from api.routers.ragify import router


def init_routers(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(router_2)


def create_app() -> FastAPI:
    app = FastAPI(
        title='RAG API',
        description='bişiler burası detay',
        version='1.0.0',
    )
    init_routers(app)
    return app

# CORSMiddleware


app = create_app()