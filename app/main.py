import asyncio
import os
import uuid
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from app.application.generation import GenerationService
from app.application.routing import RoutingService
from app.core.di import get_dependency
from app.core.interceptors import LoggingInterceptor
from app.core.logger import logger
from app.domain.data import TextData, OptionData
from app.domain.generation import GenerationOptions, GenerationRequest
from app.domain.routing import RoutingRequest
from app.generated.v1.executor import service_pb2_grpc, generation_pb2, routing_pb2, service_pb2, common_pb2


class ExecutorService(service_pb2_grpc.ExecutorServiceServicer):
    def __init__(self):
        self.generation_service = get_dependency(GenerationService)
        self.routing_service = get_dependency(RoutingService)

    def Generate(
            self,
            request: generation_pb2.GenerationRequest,
            context: grpc.ServicerContext) -> generation_pb2.GenerationResponse:
        request = GenerationRequest(
            input=TextData(text=request.input.text),
            options=GenerationOptions(
                use_memory=request.options.use_memory,
                response_json_schema=request.options.response_json_schema
            ),
            context_id=uuid.UUID(request.context_id)
        )

        try:
            result = asyncio.run(self.generation_service.generate(request))
            logger.info(f"Generated output: {result.generated_output.text}")
            return generation_pb2.GenerationResponse(
                generated_output=common_pb2.TextData(text=result.generated_output.text)
            )
        except Exception as e:
            return generation_pb2.GenerationResponse(
                error=str(e)
            )

    def Route(
            self,
            request: routing_pb2.RoutingRequest,
            context: grpc.ServicerContext) -> routing_pb2.RoutingResponse:
        request = RoutingRequest(
            input=TextData(text=request.input.text),
            options=[OptionData(option=opt.option) for opt in request.options]
        )

        try:
            result = asyncio.run(self.routing_service.route(request))
            logger.info(f"Selected option: {result.selected_option.option}")
            return routing_pb2.RoutingResponse(
                selected_option=common_pb2.OptionData(option=result.selected_option.option),
                is_fallback=result.is_fallback
            )
        except Exception as e:
            return routing_pb2.RoutingResponse(
                error=str(e)
            )


async def serve():
    server = grpc.aio.server(
        interceptors=[LoggingInterceptor()]
    )

    service_pb2_grpc.add_ExecutorServiceServicer_to_server(
        ExecutorService(), server
    )

    # Enable reflection for development environment
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "development":
        service_names = (
            service_pb2.DESCRIPTOR.services_by_name["ExecutorService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(service_names, server)
        logger.info("Reflection enabled for development environment")

    # Start the server
    server.add_insecure_port('[::]:50051')
    logger.info("Starting Chatbot Builder Executor gRPC server on port 50051 with reflection enabled")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
