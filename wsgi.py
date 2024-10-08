from fastapi import FastAPI
from api.routers.ragify import router

def init_routers(app: FastAPI) -> None:
    app.include_router(router)

def create_app() -> FastAPI:
    app = FastAPI(
        title='RAG API',
        description='bişiler burası detay',
        version='1.0.0',
    )
    init_routers(app)
    return app

app = create_app()
