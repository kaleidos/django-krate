from django.core.management import call_command

call_command('syncdb', interactive=False)

from .test_ratehandlers import *
from .test_templatetags import *
