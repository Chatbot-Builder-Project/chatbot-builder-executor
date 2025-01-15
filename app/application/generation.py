import json

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.application.abstract.langchain import ChatModelFactory
from app.application.abstract.services import GenerationService
from app.domain.data import TextData
from app.domain.generation import GenerationResponse, GenerationRequest


class DefaultGenerationService(GenerationService):
    def __init__(self, chat_model_factory: ChatModelFactory):
        self.chat_model_factory = chat_model_factory

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = self.chat_model_factory.get_chat_model()
        response_json_schema = request.options.response_json_schema

        if response_json_schema is None or len(response_json_schema) == 0:
            prompt = PromptTemplate(
                template="{query}",
                input_variables=["query"],
            )
            chain = prompt | model | StrOutputParser()
        else:
            schema_dict = json.loads(response_json_schema)
            parser = JsonOutputParser(schema=schema_dict)
            prompt = PromptTemplate(
                template="{query}\n{format_instructions}",
                input_variables=["query"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
            chain = prompt | model | parser

        response = await chain.ainvoke({"query": request.input.text})

        return GenerationResponse(
            generated_output=TextData(text=str(response))
        )
