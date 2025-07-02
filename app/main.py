import sys
from typing import cast

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.routers import api_router
from app.config import settings
from app.exceptions.custom_exception import CustomException

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


def custom_exception_handler(request, exception):
    e = cast(CustomException, exception)
    logger.error("error * [{}/{}]", e.status_code, e.message)

    return JSONResponse({"detail": e.message}, status_code=e.status_code)


def exception_handler(request, exception):
    logger.error("uncaught exception * {}", sys.exc_info())

    return JSONResponse(status_code=500, content={"detail": str(exception)})


app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT, workers=1)
