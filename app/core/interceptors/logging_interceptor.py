import time
from typing import Callable

import grpc
from grpc_interceptor import ServerInterceptor

from app.core.logger import logger


class LoggingInterceptor(ServerInterceptor):
    def intercept(self, method: Callable, request: any, context: grpc.ServicerContext, method_name: str) -> any:
        start_time = time.time()
        logger.info(f"Request: {method_name}")

        try:
            response = method(request, context)
            process_time = time.time() - start_time
            logger.info(f"Response: Success (Time: {process_time:.2f}s) - {response}")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Response: Error (Time: {process_time:.2f}s) - {str(e)}")
            raise
