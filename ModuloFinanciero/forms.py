from django import forms
from .models import SolicitudCredito

class SolicitudForm(forms.ModelForm):
    hash = forms.CharField(widget=forms.HiddenInput(), initial={'hash': ''})
    class Meta:
        model = SolicitudCredito
        fields = "__all__"