from abc import abstractmethod, ABC

from app.domain.generation import GenerationRequest, GenerationResponse
from app.domain.routing import RoutingRequest, RoutingResponse


class GenerationService(ABC):
    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        pass


class RoutingService(ABC):
    @abstractmethod
    async def route(self, request: RoutingRequest) -> RoutingResponse:
        pass
