import time
import json
import logging
from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("crm")


async def request_logger(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={process_time:.4f}s"
    )

    return response


async def response_wrapper(request: Request, call_next):

    response = await call_next(request)

    if (
        request.url.path.startswith("/docs")
        or request.url.path.startswith("/openapi.json")
        or request.url.path.startswith("/redoc")
    ):
        return response

    if response.headers.get("content-type") == "application/json":
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        data = json.loads(body)

        return JSONResponse(
            status_code=response.status_code, content={"success": True, "data": data}
        )

    return response
