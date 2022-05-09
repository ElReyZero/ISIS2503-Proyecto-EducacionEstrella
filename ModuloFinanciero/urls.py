from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('solicitud/create', views.solicitud_create, name='solicitudCreate'),
    path('solicitud/create_exempt', views.solicitud_create_csrf_exempt, name='solicitudCreateExempt'),
    path('solicitud/<id>', views.solicitud_view, name='solicitud'),
]