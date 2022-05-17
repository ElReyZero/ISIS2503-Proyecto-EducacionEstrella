from django.db import models
# Create your models here.

class EstudianteEstrella(models.Model):
    nombre = models.CharField(max_length=50, null=False, default="")
    carrera = models.CharField(max_length=50, null=False, default="")
    ciudad = models.CharField(max_length=50, null=False, default="")
    universidad = models.CharField(max_length=50, null=False, default="")
    genero = models.CharField(max_length=50, null=False, default="")
    edad = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.nombre


class SolicitudCredito(models.Model):
    estudiante = models.ForeignKey(EstudianteEstrella, on_delete=models.CASCADE)
    analista = models.CharField(max_length=50, null=False, default="N/A")
    montoAPagar = models.DecimalField(max_digits=10, decimal_places=2)
    fechaSolicitud = models.DateTimeField(auto_now_add=True)
    fechaAprobacion = models.DateTimeField(null=True)
    pagado = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"Solicitud de Credito de: {self.estudiante}"