from django.db import models

class JobListing(models.Model):
    titulo = models.CharField(max_length=50)
    carrera = models.CharField(max_length=50)
    empresa = models.CharField(max_length=100)
    tipoDeTrabajo = models.CharField(max_length=50)
    industria = models.CharField(max_length=50)
    tipoExperiencia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    salario = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.titulo}"
