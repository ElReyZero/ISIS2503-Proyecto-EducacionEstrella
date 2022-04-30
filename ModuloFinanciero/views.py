from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from EducacionEstrella.auth0backend import getRole
from .logic.solicitud_logic import get_solicitudes, get_solicitud, create_solicitud
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SolicitudForm

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


@login_required
def solicitud_create(request):
    role = getRole(request)
    if role == "AnalistaCredito":
        if request.method == 'POST':
            form = SolicitudForm(request.POST)
            if form.is_valid():
                create_solicitud(form)
                messages.add_message(request, messages.SUCCESS, 'Successfully created Solicitud')
                return HttpResponseRedirect(reverse('solicitudCreate'))
            else:
                print(form.errors)
        else:
            form = SolicitudForm()

        context = {
            'form': form,
        }
        return render(request, 'ModuloFinanciero/solicitudCreate.html', context)
    else:
        return HttpResponseForbidden()
