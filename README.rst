Django Kaleidos Rate
====================

.. image:: https://travis-ci.org/kaleidos/django-krate.png?branch=master
    :target: https://travis-ci.org/kaleidos/django-krate

.. image:: https://coveralls.io/repos/kaleidos/django-krate/badge.png?branch=master
    :target: https://coveralls.io/r/kaleidos/django-krate?branch=master

.. image:: https://pypip.in/v/django-krate/badge.png
    :target: https://crate.io/packages/django-krate

.. image:: https://pypip.in/d/django-krate/badge.png
    :target: https://crate.io/packages/django-krate


Django Kaleidos Rate is a django application for rate objects.

Configuration
-------------

Configure the app in your setting INSTALLED_APPS::

  INSTALLED_APPS = [
     ...
     krate,
     ...
  ]


DBRateHandler configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

configure the dbratehandler, for example::

  INSTALLED_APPS = [
     ...
     krate.ratehandlers.dbratehandler,
     ...
  ]

Configure the rate handler on settings.py, for example::

  KRATE_RATE_HANDLER = "krate.ratehandlers.dbratehandler.DBRateHandler"

If you want to have an copy of the average rate stored in the models add the
KRateableMixin to your models, for example::

  from krate.ratehandlers.dbratehandler.models import KRateableMixin

  class MyModel(models.Model, KRateableMixin):
      ... # My model definition...

If you want to show and manage the valorations of the objects in the admin
panel add a new inline to your models admin classes, for example:: 

  from django.contrib.contenttypes.generic import GenericTabularInline
  from krate.ratehandlers.dbratehandler.models import ObjRate, ObjRateAggregate

  class ObjRateInline(GenericTabularInline):
      model = ObjRate

  class ObjRateAggregateInline(GenericTabularInline):
      model = ObjRateAggregate
  
  class MyModelAdmin(admin.ModelAdmin):
      model = models.MyModel
      inlines = [MyOtherInlines, ...,  ObjRateAggregateInline, ObjRateAggregateInline]

Usage
-----

Now you can use rate_object in your views to store the rate from users, and use
the {% krate object %} and {% mykrate request_or_user object %} to get the average rate, and my
own rate.
