from contextvars import ContextVar

import pytz
from loguru import logger
import json
from datetime import datetime

from app.settings import get_settings

TZ = pytz.timezone(get_settings().TIMEZONE)

trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)

def file_sink(message):
    record = message.record
    extra = record["extra"]

    data = {}

    if record["message"] and record["message"] != "message":
        data["event"] = record["message"]

    masked_extra = mask_sensitive_fields(extra)

    if "data" in masked_extra and isinstance(masked_extra["data"], dict):
        data.update(masked_extra["data"])
        del masked_extra["data"]

    data.update(masked_extra)

    base = {
        "timestamp": datetime.now(TZ).isoformat(),
        "level": record["level"].name,
        "data": data,
    }

    with open("logs/log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(base, ensure_ascii=False) + "\n")

logger.add(
    "logs/log.json",
    level="DEBUG",
    enqueue=True,
    serialize=True,
    filter=lambda record: record["extra"].get("server") == "grpc")


def mask_sensitive_fields(data):
    def recursive_mask(obj):
        if isinstance(obj, dict):
            return {
                k: "***MASKED***" if k in ("user_id", "userId") else recursive_mask(v)
                for k, v in obj.items()
            }
        else:
            return obj
    return recursive_mask(data)

def get_logger():
    trace_id = trace_id_var.get()
    return logger.bind(trace_id=trace_id) if trace_id else logger

logger.remove()

logger.add(
    file_sink,
    level="DEBUG",
    enqueue=True)
