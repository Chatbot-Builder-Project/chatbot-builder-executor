from fastapi import FastAPI
from app.api.v1.routers.test_router import router as test_router

# Create the FastAPI application
app = FastAPI(
    title="Chatbot Builder Engine API",
    description="The execution engine for the Chatbot Builder.",
    version="1.0.0"
)

# Register the controllers
app.include_router(test_router, prefix="/v1", tags=["Test"])
