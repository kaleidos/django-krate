from krate.ratehandlers.dbratehandler.models import KRateableMixin
from django.db import models

class TestModel(KRateableMixin):
    pass

class TestModel2(models.Model):
    pass
