from krate import settings
from django.utils.importlib import import_module

__all__ = ('ratehandler',)

module_name = ".".join(settings.KRATE_RATE_HANDLER.split(".")[0:-1])
class_name = settings.KRATE_RATE_HANDLER.split(".")[-1]
ratehandler = getattr(import_module(module_name), class_name)()
