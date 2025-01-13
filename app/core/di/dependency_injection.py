from injector import Binder, Injector

from app.application.abstract.services import GenerationService, RoutingService
from app.application.generation import DefaultGenerationService
from app.application.routing import DefaultRoutingService


# Configure the dependency injection container
def configure(binder: Binder) -> None:
    binder.bind(GenerationService, to=DefaultGenerationService)
    binder.bind(RoutingService, to=DefaultRoutingService)
    pass


injector = Injector([configure])


def get_dependency(dep):
    return injector.get(dep)
