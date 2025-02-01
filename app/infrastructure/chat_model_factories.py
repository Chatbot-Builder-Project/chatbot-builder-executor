from langchain_openai import AzureChatOpenAI, ChatOpenAI

from app.application.abstract.langchain import ChatModelFactory


class AzureChatModelFactory(ChatModelFactory):
    """
    Factory implementation for Azure OpenAI chat models.
    """

    def __init__(
            self,
            endpoint: str,
            api_key: str,
            deployment_name: str,
            api_version: str = "gpt-4o-2024-11-20"):
        """
        Initialize the factory with Azure OpenAI configuration.

        :param endpoint: Azure OpenAI endpoint.
        :param api_key: Azure OpenAI API key.
        :param deployment_name: The deployment name of the chat model in Azure.
        :param api_version: API version for Azure OpenAI (default is "2023-03-15-preview").
        """
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.api_version = api_version

    def get_chat_model(self) -> AzureChatOpenAI:
        """
        Create and return an AzureChatOpenAI instance.

        :return: Instance of AzureChatOpenAI.
        """
        return AzureChatOpenAI(
            deployment_name=self.deployment_name,  # must be implemented in terraform
            openai_api_base=self.endpoint,
            openai_api_key=self.api_key,
            openai_api_version=self.api_version
        )


class DeepSeekChatModelFactory(ChatModelFactory):
    """
    Factory implementation for DeepSeek chat models.
    """

    def __init__(self, endpoint: str, api_key: str):
        """
        Initialize the factory with DeepSeek configuration.

        :param endpoint: DeepSeek endpoint.
        :param api_key: DeepSeek API key.
        """
        self.endpoint = endpoint
        self.api_key = api_key

    def get_chat_model(self) -> ChatOpenAI:
        """
        Create and return a DeepSeekChat instance.

        :return: Instance of DeepSeekChat.
        """
        return ChatOpenAI(
            model="gpt-4o-mini-2024-07-18",
            openai_api_key=self.api_key,
            openai_api_base=self.endpoint,
        )
