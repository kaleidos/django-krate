from django.conf import settings

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class ObjRate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    krate = models.FloatField(null=True, blank=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)

class ObjRateAggregate(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    summatory = models.FloatField(null=False, blank=False, default=0)
    count = models.IntegerField(null=False, blank=False, default=0)
    avg = models.FloatField(null=True, blank=True, default=None)

class KRateableMixin(models.Model):
    krate = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        abstract = True
