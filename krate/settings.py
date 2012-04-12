from django.conf import settings

KRATE_RATE_HANDLER = getattr(settings, 'KRATE_RATE_HANDLER', 'krate.ratehandlers.noratehandler.NoRateHandler')
KRATE_DEFAULT_CHOICES = getattr(settings, 'KRATE_DEFAULT_CHOICES', [1, 2, 3, 4, 5])
