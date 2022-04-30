from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('solicitud/create', views.solicitud_create, name='solicitudCreate'),
    path('solicitud/<id>', views.solicitud_view, name='solicitud'),
]