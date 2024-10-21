from fastapi import Request
from app.core.logger import logger
import time


async def log_request_response_middleware(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")

    # Call the next handler
    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} (Time: {process_time:.2f}s)")

    return response
