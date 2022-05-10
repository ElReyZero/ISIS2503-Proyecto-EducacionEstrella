from rest_framework import serializers
from . import models
class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.JobListing

class EmpresaSerializer(serializers.ModelSerializer):  
    class Meta:
        fields = '__all__'
        model = models.Empresa

class SolicitudEmpleoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SolicitudesEmpleo