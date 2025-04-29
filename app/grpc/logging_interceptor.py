import time
from uuid import uuid4
import grpc
from google.protobuf.json_format import MessageToDict

from app.core.logger import trace_id_var, get_logger, mask_sensitive_fields


class LoggingInterceptor(grpc.aio.ServerInterceptor):

    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata or [])

        trace_id = metadata.get("x-trace-id", str(uuid4()))
        trace_id_var.set(trace_id)
        logger_ctx = get_logger()

        logger_ctx.bind(data={
            "server": "grpc",
            "type": "request",
            "method": method,
            "metadata": metadata,
        }).info("message")

        try:
            handler = await continuation(handler_call_details)

            async def new_behavior(request, context):
                start_time = time.monotonic()

                logger_ctx.bind(**mask_sensitive_fields({
                        "server": "grpc",
                        "type": "request_body",
                        "method": method,
                        "request": MessageToDict(request),
                    })).debug("request data")

                response = await handler.unary_unary(request, context)

                elapsed = (time.monotonic() - start_time)

                logger_ctx.bind(**mask_sensitive_fields({
                    "server": "grpc",
                    "type": "response",
                    "method": method,
                    "status": grpc.StatusCode.OK.name,
                    "duration": round(elapsed, 2),
                    "response_size_bytes": len(response.SerializeToString()),
                    "client_ip": context.peer().split(":")[1]
                })).info("message")

                return response

            return grpc.unary_unary_rpc_method_handler(
                new_behavior,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer
            )

        except Exception as e:
            logger_ctx.bind(data={
                "server": "grpc",
                "type": "error",
                "method": method,
                "error": str(e),
            }).error("message")
            raise
