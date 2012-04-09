from .ratehandlerbase import RateHandlerBase

class NoRateHandler(RateHandlerBase):
    def rate_object(self, request, obj, rate, **kwargs):
        return ('created', 0)

    def get_object_rate(self, obj, **kwargs):
        return 0

    def get_request_object_rate(self, user, obj, **kwargs):
        return 0

    def get_user_object_rate(self, user, obj, **kwargs):
        return 0
