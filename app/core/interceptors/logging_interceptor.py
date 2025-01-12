import time
from typing import Callable, Any
import grpc

from app.core.logger import logger


class LoggingInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(
            self,
            continuation: Callable[[grpc.HandlerCallDetails], Any],
            handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:
        start_time = time.time()
        method_name = handler_call_details.method
        logger.info(f"Request: {method_name}")

        try:
            response = await continuation(handler_call_details)
            process_time = time.time() - start_time
            logger.info(f"Response: Success (Time: {process_time:.2f}s)")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Response: Error (Time: {process_time:.2f}s) - {str(e)}")
            raise
