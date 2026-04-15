from fastapi import Request
from fastapi.responses import JSONResponse
import json


async def response_wrapper(request: Request, call_next):
    response = await call_next(request)

    if response.headers.get("content-type") == "application/json":
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        data = json.loads(body)

        return JSONResponse(
            status_code=response.status_code, content={"success": True, "data": data}
        )

    return response
