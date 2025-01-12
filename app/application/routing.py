from abc import abstractmethod, ABC

from app.domain.routing import RoutingRequest, RoutingResponse


class RoutingService(ABC):
    @abstractmethod
    async def route(self, request: RoutingRequest) -> RoutingResponse:
        pass


class DefaultRoutingService(RoutingService):
    async def route(self, request: RoutingRequest) -> RoutingResponse:
        return RoutingResponse(
            selected_option=request.options[0] if request.options else "",
            is_fallback=False
        )
