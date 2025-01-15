from enum import Enum
import re

from langchain.output_parsers import EnumOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.application.abstract.langchain import ChatModelFactory
from app.application.abstract.services import RoutingService
from app.core.logger import logger
from app.domain.data import OptionData
from app.domain.routing import RoutingRequest, RoutingResponse


def normalize_option(option: str) -> str:
    # Replace any sequence of whitespace (space, tabs, etc.) with a single underscore
    normalized = re.sub(r'\s+', '_', option)
    # Remove any non-alphanumeric characters (except underscores) and uppercase
    normalized = re.sub(r'\W', '', normalized).upper()
    return normalized


class DefaultRoutingService(RoutingService):
    def __init__(self, chat_model_factory: ChatModelFactory):
        self.chat_model_factory = chat_model_factory

    async def route(self, request: RoutingRequest) -> RoutingResponse:
        option_to_key = {option.option: normalize_option(option.option) for option in request.options}
        key_to_option = {v: k for k, v in option_to_key.items()}

        prompt = PromptTemplate(
            template="""
            {query}
            
            Don't explain your answer.
            Respond only with a single word or phrase from the following options:
            {options}
            """,
            input_variables=["query"],
            partial_variables={"options": "\n".join([key for key in key_to_option.keys()])}
        )

        model = self.chat_model_factory.get_chat_model()
        chain = prompt | model | StrOutputParser()

        answer = await chain.ainvoke({"query": request.input.text})

        for key, option in key_to_option.items():
            if key in answer:
                return RoutingResponse(
                    selected_option=OptionData(option=option),
                    is_fallback=False
                )

        logger.warning(f"Failed to parse response for input: {request.input.text}\n"
                       f"Options: {option_to_key}\n"
                       f"LLM Response: {answer}")

        return RoutingResponse(
            selected_option=OptionData(option="Fallback"),
            is_fallback=True
        )
