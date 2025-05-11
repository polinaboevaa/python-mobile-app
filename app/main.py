import asyncio
import time
from uuid import uuid4
from typing import AsyncGenerator, Any

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.settings import get_base_settings, get_settings
from app.transports.router import router as schedule_router
from app.core.logger import trace_id_var, get_logger
from app.grpc.server import start_grpc_server


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:

    core_settings = get_base_settings()
    db_settings = get_settings()

    grpc_server_task = asyncio.create_task(start_grpc_server(db_settings, core_settings))
    try:
        yield {}
    finally:
        grpc_server_task.cancel()
        try:
            await grpc_server_task
        except asyncio.CancelledError:
            pass


def make_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    app.include_router(schedule_router)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        trace_id = request.headers.get("X-TRACE-ID") or str(uuid4())
        trace_id_var.set(trace_id)

        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        logger = get_logger()

        logger.bind(data={
            "server": "rest",
            "type": "request",
            "method": request.method,
            "url": str(request.url),
            "client_ip": client_ip,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
        }).info("message")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.bind(data={
            "server": "rest",
            "type": "response",
            "status_code": response.status_code,
            "duration": round(process_time, 4),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "content_length": response.headers.get("content-length", "unknown"),
        }).info("message")

        return response

    return app
