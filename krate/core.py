from . import settings
from .ratehandlers import ratehandler

def rate_object(request, obj, rate, **kwargs):
    ratehandler.rate_object(request, obj, rate, **kwargs)

def get_object_rate(request, obj, **kwargs):
    ratehandler.get_object_rate(request, obj, **kwargs)

def get_request_object_rate(request, obj, **kwargs):
    ratehandler.get_object_rate(request, obj, **kwargs)

def get_user_object_rate(user, obj, **kwargs):
    ratehandler.get_object_rate(user, obj, **kwargs)
