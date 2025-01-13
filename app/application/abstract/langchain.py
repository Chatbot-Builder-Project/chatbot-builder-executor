from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel


class ChatModelFactory(ABC):
    """
    Abstract factory for creating LangChain chat model instances.
    """

    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        """
        :return: Instance of a LangChain BaseChatModel.
        """
        pass
