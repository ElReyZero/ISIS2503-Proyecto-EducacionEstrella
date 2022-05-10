from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.jobListing_list),
    path('create', csrf_exempt(views.job_listing_create), name ='jobListingCreate'),
    path('<str:major>', views.jobListing_get_by_major, name='jobListingGetByMajor'),
    path('empresa/create', views.empresa_create, name='empresaCreate'),
    path('solicitud/create', views.solicitudEmpleo_create, name='solicitudEmpleoCreate'),
]