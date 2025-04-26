from uuid import uuid4

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.database.database import create_tables
from app.api.router import router as schedule_router
from app.core.logger import trace_id_var, get_logger
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(schedule_router)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    trace_id = request.headers.get("X-TRACE-ID")
    if not trace_id:
        trace_id = str(uuid4())

    trace_id_var.set(trace_id)

    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")

    logger_ctx = get_logger()

    request_data = {
        "type": "request",
        "method": request.method,
        "url": str(request.url),
        "client_ip": client_ip,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
    }
    logger_ctx.bind(data=request_data).info("message")

    response = await call_next(request)
    process_time = time.time() - start_time

    response_data = {
        "type": "response",
        "status_code": response.status_code,
        "duration": round(process_time, 4),
        "client_ip": client_ip,
        "user_agent": user_agent,
        "content_length": response.headers.get("content-length", "unknown"),
    }
    logger_ctx.bind(data=response_data).info("message")

    return response

