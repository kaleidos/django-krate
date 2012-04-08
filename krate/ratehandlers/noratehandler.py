from .ratehandlerbase import RateHandlerBase

class NoRateHandler(RateHandlerBase):
    def rate_object(self, request, obj, rate, **kwargs):
        return None

    def get_object_rate(self, request, obj, **kwargs):
        return 0

    def get_request_object_rate(self, user, obj, **kwargs):
        return 0

    def get_user_object_rate(self, user, obj, **kwargs):
        return 0
