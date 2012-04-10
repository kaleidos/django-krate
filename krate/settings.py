from django.conf import settings

KRATE_RATE_HANDLER = getattr(settings, 'KRATE_RATE_HANDLER', 'krate.ratehandlers.noratehandler.NoRateHandler')
