from app.application.abstract.services import GenerationService
from app.domain.data import TextData
from app.domain.generation import GenerationResponse, GenerationRequest


class DefaultGenerationService(GenerationService):
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        return GenerationResponse(
            generated_output=TextData(text=f"Generated text for {request.input.text}")
        )
