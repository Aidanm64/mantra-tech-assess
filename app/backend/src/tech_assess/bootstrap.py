import inspect
from functools import wraps

from typing import Callable
from tech_assess.service import UnitOfWork, MessageBus, handlers
from tech_assess.service.unit_of_work import MongoUnitOfWork
from tech_assess.adapters import external_bus, combiner


def bootstrap(
    uow: UnitOfWork=MongoUnitOfWork(),
    publish: Callable=external_bus.publish,
    combiner: combiner.Combiner=combiner.MockCombiner()
) -> MessageBus:

    dependencies = {
        'uow': uow,
        'publish': publish,
        'combiner': combiner}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
