from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import auth, cravings, tasks, eco, rl

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_prefix = settings.api_v1_prefix
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(cravings.router, prefix=api_prefix)
    app.include_router(tasks.router, prefix=api_prefix)
    app.include_router(eco.router, prefix=api_prefix)
    app.include_router(rl.router, prefix=api_prefix)

    @app.get("/")
    async def root():
        return {"status": "ok", "name": settings.app_name}

    return app


app = create_app()
