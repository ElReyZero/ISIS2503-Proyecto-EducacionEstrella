from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from EducacionEstrella.auth0backend import getRole
from .logic.solicitud_logic import get_solicitudes, get_solicitud, create_solicitud
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SolicitudForm
import requests
import urllib3
@login_required
def dashboard_view(request):
    role = getRole(request)
    if role == "AnalistaCredito":
        solicitudes = get_solicitudes()
        context = {
            'solicitudes_list': solicitudes
        }
        return render(request, 'ModuloFinanciero/solicitudes.html', context)
    else:
        return HttpResponseForbidden()

@login_required
def solicitud_view(request, id=0):
    role = getRole(request)
    if role == "AnalistaCredito":
        solicitud = get_solicitud(id)
        context = {
            'solicitud': solicitud
        }
        return render(request, 'ModuloFinanciero/solicitud.html', context)
    else:
        return HttpResponseForbidden()

def solicitud_create(request):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.cleaned_data["estudiante"] = "Jairo Molano"
            form.cleaned_data["montoAPagar"] = "100000"
            form.cleaned_data["fechaAprobacion"] = "2022-01-01"
            # Ejemplo con toda protección
            r_protected = requests.post("https://54.161.20.94/modulo-financiero/solicitud/create", data=form.cleaned_data, cookies=request.COOKIES, verify=False)
            print(r_protected.text)
            print(r_protected.status_code)
            # Ejemplo CSRF_EXEMPT
            r_no_csrf = requests.post("https://54.161.20.94/modulo-financiero/solicitud/create_exempt", data=form.cleaned_data, cookies=request.COOKIES, verify=False)
            print(r_no_csrf.text)
            print(r_no_csrf.status_code)
            # Ejemplo sin protección
            r_no_protected = requests.post("https://54.161.20.94/modulo-financiero/solicitud/create_insecure", data=form.cleaned_data, cookies=request.COOKIES, verify=False)
            print(r_no_protected.text)
            print(r_no_protected.status_code)
            return HttpResponseRedirect(reverse('solicitudCreate'))
        else:
            print(form.errors)
    else:
        form = SolicitudForm()

    context = {
        'form': form,
    }
    return render(request, 'ModuloFinanciero/solicitudCreate.html', context)