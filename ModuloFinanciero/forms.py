from django import forms
from .models import SolicitudCredito

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudCredito
        fields = "__all__"