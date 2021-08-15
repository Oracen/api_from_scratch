import sys
from typing import Any, Dict, List
from fastapi import FastAPI, Request
from loguru import logger
from starlette.routing import Match

from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware.cors import CORSMiddleware

from api_from_scratch.api.fixed_returns import API_VERSIONS
from api_from_scratch.api.v1.router import router_v1
from api_from_scratch.structs.responses.api_root import ResponseApiRoot

"""
This module serves to import all the elements of the main API, routers etc. into
a single app that can be served.

Authentication is missing as implementing the middleware will take a while
"""
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
)


app = FastAPI(debug=True)

app.include_router(router_v1, prefix="/v1", tags=["api-v1"])


@app.get("/")
async def get_api_versions() -> ResponseApiRoot:
    """
    Return all valid API versions.

    Returns:
        List<str>: a list of all valid API versions
    """
    # TODO: Change this to all valid API methods without docs
    return ResponseApiRoot(message="OK", versions=API_VERSIONS)


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    response = await call_next(request)
    return response


# Quick hack to enable development
# TODO: Set CORS properly

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://127.0.0.1:8080",
        "http://localhost",
        "http://localhost:*",
        "https://localhost:*",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
    allow_headers=["*"],
)
