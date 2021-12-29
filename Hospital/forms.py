# from django import forms
from django.forms.models import ModelForm
# from django.forms import fields
from .models import Measurement


class MeasurementModelForm(ModelForm):
    class Meta:
        model = Measurement
        fields = ('donorLocation',)