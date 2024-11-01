from injector import Binder, Injector


# Configure the dependency injection container
def configure(binder: Binder) -> None:
    # binder.bind(MyServiceInterface, to=MyService, scope=singleton)
    pass


injector = Injector([configure])


def get_dependency(dep):
    return injector.get(dep)
