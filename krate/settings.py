from django.conf import settings

KRATE_RATE_HANDLER = getattr(settings, 'KRATE_RATE_HANDLER', 'kvisits.counterhandlers.nocounterhandler.NoRateHandler')
