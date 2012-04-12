from django.db import transaction
from ..ratehandlerbase import RateHandlerBase
from .models import *

class DBRateHandler(RateHandlerBase):
    def rate_object(self, request, obj, rate, **kwargs):
        with transaction.commit_on_success():
            try:
                rate = float(rate)
            except ValueError:
                return ('invalid-rate-format', rate)
            obj_content_type = ContentType.objects.get_for_model(obj)
            (obj_rate, created) = ObjRate.objects.get_or_create(content_type=obj_content_type, object_id=obj.pk, user=request.user)
            (obj_rate_aggregate, created_agg) = ObjRateAggregate.objects.get_or_create(content_type=obj_content_type, object_id=obj.pk)

            if created_agg:
                obj_rate.krate = rate
                obj_rate.save()
                obj_rate_aggregate.count = 1
                obj_rate_aggregate.summatory = rate
                obj_rate_aggregate.avg = rate
                obj_rate_aggregate.save()
                if isinstance(obj, KRateableMixin):
                    obj.krate = rate
                    obj.save()
                return ('created', rate)
            elif not created_agg and created:
                obj_rate.krate = rate
                obj_rate.save()
                obj_rate_aggregate.count += 1
                obj_rate_aggregate.summatory += rate
                obj_rate_aggregate.avg = obj_rate_aggregate.summatory / obj_rate_aggregate.count
                obj_rate_aggregate.save()
                if isinstance(obj, KRateableMixin):
                    obj.krate = obj_rate_aggregate.avg
                    obj.save()
                return ('created', obj_rate_aggregate.avg)
            elif not created_agg and not created:
                obj_rate_aggregate.summatory -= obj_rate.krate
                obj_rate_aggregate.summatory += rate
                obj_rate_aggregate.avg = obj_rate_aggregate.summatory / obj_rate_aggregate.count
                obj_rate_aggregate.save()
                obj_rate.krate = rate
                obj_rate.save()
                if isinstance(obj, KRateableMixin):
                    obj.krate = obj_rate_aggregate.avg
                    obj.save()
                return ('modified', obj_rate_aggregate.avg)

    def get_object_rate(self, obj, **kwargs):
        if isinstance(obj, KRateableMixin):
            return obj.krate
        else:
            try:
                obj_content_type = ContentType.objects.get_for_model(obj)
                obj_rate = ObjRateAggregate.objects.get(content_type=obj_content_type, object_id=obj.pk)
                return obj_rate.avg
            except ObjVisit.DoesNotExist:
                return None

    def get_request_object_rate(self, request, obj, **kwargs):
        return self.get_user_object_rate(request.user, obj, **kwargs)

    def get_user_object_rate(self, user, obj, **kwargs):
        try:
            obj_content_type = ContentType.objects.get_for_model(obj)
            obj_rate = ObjRate.objects.get(content_type=obj_content_type, object_id=obj.pk, user=user)
            return obj_rate.krate
        except ObjRate.DoesNotExist:
            return None
