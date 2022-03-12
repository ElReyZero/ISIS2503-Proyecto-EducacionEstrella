from rest_framework import serializers
from . import models
class JobListingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'titulo', 'carrera', 'empresa', 'tipoDeTrabajo', 'industria', 'tipoExperiencia', 'descripcion', 'salario')
        model = models.JobListing