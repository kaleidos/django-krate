from . import settings
from .ratehandlers import ratehandler

def rate_object(request, obj, rate, **kwargs):
    return ratehandler.rate_object(request, obj, rate, **kwargs)

def get_object_rate(obj, **kwargs):
    return ratehandler.get_object_rate(obj, **kwargs)

def get_request_object_rate(request, obj, **kwargs):
    return ratehandler.get_request_object_rate(request, obj, **kwargs)

def get_user_object_rate(user, obj, **kwargs):
    return ratehandler.get_user_object_rate(user, obj, **kwargs)
