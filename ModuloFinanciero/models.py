from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SolicitudCredito(models.Model):
    estudiante = models.CharField(max_length=50, null=False, default="N/A")
    analista = models.CharField(max_length=50, null=False, default="N/A")
    montoAPagar = models.DecimalField(max_digits=10, decimal_places=2)
    fechaSolicitud = models.DateTimeField(auto_now_add=True)
    fechaAprobacion = models.DateTimeField(null=True)

    def __str__(self):
        return f"Solicitud de Credito de: {self.estudiante}"