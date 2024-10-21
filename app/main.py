from fastapi import FastAPI
from app.api.v1.routers.test_router import router as test_router
from app.core.middlewares import log_request_response_middleware

# Create the FastAPI application
app = FastAPI(
    title="Chatbot Builder Engine API",
    description="The execution engine for the Chatbot Builder.",
    version="1.0.0"
)

# Register the middlewares
app.middleware("http")(log_request_response_middleware)

# Register the controllers
app.include_router(test_router, prefix="/v1", tags=["Test"])
