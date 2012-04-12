from django import forms
from .settings import *
from django.forms.widgets import RadioSelect

KRATE_CHOICES = [ (x,str(x)) for x in KRATE_DEFAULT_CHOICES ]

class KRateForm(forms.Form):
    value = forms.ChoiceField(widget=forms.widgets.RadioSelect,
                              choices=KRATE_CHOICES)
