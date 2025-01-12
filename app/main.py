import os
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from app.core.interceptors import LoggingInterceptor
from app.generated.v1.executor import service_pb2_grpc, generation_pb2, routing_pb2, service_pb2, common_pb2

from app.core.logger import logger


# Service implementation
class ExecutorService(service_pb2_grpc.ExecutorServiceServicer):
    def Generate(self, request: generation_pb2.GenerationRequest,
                 context: grpc.ServicerContext) -> generation_pb2.GenerationResponse:
        text = request.input.text
        use_memory = request.options.use_memory
        response_schema = request.options.response_json_schema

        # Your generation logic here
        generated_text = f"Generated response for: {text}"  # Placeholder

        return generation_pb2.GenerationResponse(
            generated_output=common_pb2.TextData(text=generated_text)
        )

    def Route(self, request: routing_pb2.RoutingRequest,
              context: grpc.ServicerContext) -> routing_pb2.RoutingResponse:
        text = request.input.text
        options = [opt.option for opt in request.options]

        # Your routing logic here
        selected = options[0] if options else ""
        is_fallback = False

        return routing_pb2.RoutingResponse(
            selected_option=common_pb2.OptionData(option=selected),
            is_fallback=is_fallback
        )


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
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
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
