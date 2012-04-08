class RateHandlerBase(object):
    def rate_object(self, request, obj, rate, **kwargs):
        raise NotImplementedError

    def get_object_rate(self, request, obj, **kwargs):
        raise NotImplementedError

    def get_request_object_rate(self, request, obj, **kwargs):
        raise NotImplementedError

    def get_user_object_rate(self, user, obj, **kwargs):
        raise NotImplementedError
