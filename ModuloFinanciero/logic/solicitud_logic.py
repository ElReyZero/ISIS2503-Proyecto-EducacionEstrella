from ..models import SolicitudCredito

def get_solicitudes():
    queryset = SolicitudCredito.objects.all()
    return (queryset)

def get_solicitud(id):
    solicitud = SolicitudCredito.objects.get(id=id)
    return solicitud

def create_solicitud(form):
    solicitud = form.save()
    solicitud.save()
    return ()