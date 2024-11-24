from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import handlers
from routes import root_router
from settings import get_settings

cfg = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    from bot import start_telegram
    await start_telegram()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
