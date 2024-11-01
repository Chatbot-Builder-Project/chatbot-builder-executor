from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Simple endpoint to test the API setup.
    """
    return {"message": "pong"}


@router.get("/sentry-debug")
async def trigger_error():
    _ = 1 / 0
