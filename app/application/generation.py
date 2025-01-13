from app.application.abstract.langchain import ChatModelFactory
from app.application.abstract.services import GenerationService
from app.domain.data import TextData
from app.domain.generation import GenerationResponse, GenerationRequest


class DefaultGenerationService(GenerationService):
    def __init__(self, chat_model_factory: ChatModelFactory):
        self.chat_model_factory = chat_model_factory

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        llm = self.chat_model_factory.get_chat_model()

        chat_response = await llm.ainvoke(request.input.text)

        return GenerationResponse(
            generated_output=TextData(text=chat_response.content)
        )
