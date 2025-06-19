import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.config import settings

# Logger
logger.remove()

logger.add(
    sys.stdout,
    format="[<blue>{time:YYYY-MM-DD HH:mm:ss}</blue>][<level>{level}</level>][{name}|{function}:{line}] -> {message}",
    colorize=True,
)

app = FastAPI(
    title="evWhere API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT, workers=1)
