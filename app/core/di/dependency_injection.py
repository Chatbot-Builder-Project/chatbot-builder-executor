import os

import dotenv
from injector import Binder, Injector

from app.application.abstract.langchain import ChatModelFactory
from app.application.abstract.services import GenerationService, RoutingService
from app.application.generation import DefaultGenerationService
from app.application.routing import DefaultRoutingService
from app.infrastructure.chat_model_factories import DeepSeekChatModelFactory, AzureChatModelFactory

dotenv.load_dotenv()


# Configure the dependency injection container
def configure(binder: Binder) -> None:
    # Determine which chat model factory to use
    if os.getenv("USE_DEEPSEEK") == "true":
        chat_model_factory = DeepSeekChatModelFactory(
            endpoint=os.getenv("DEEPSEEK_ENDPOINT"),
            api_key=os.getenv("DEEPSEEK_KEY")
        )
    else:
        chat_model_factory = AzureChatModelFactory(
            endpoint=os.getenv("OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_KEY"),
            deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("OPENAI_API_VERSION")
        )
    binder.bind(ChatModelFactory, to=chat_model_factory)

    binder.bind(GenerationService, to=DefaultGenerationService(chat_model_factory))
    binder.bind(RoutingService, to=DefaultRoutingService(chat_model_factory))
    pass


injector = Injector([configure])


def get_dependency(dep):
    return injector.get(dep)
