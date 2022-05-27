from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from EducacionEstrella.auth0backend import getRole
from .logic.solicitud_logic import get_solicitudes, get_solicitud, create_solicitud
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import SolicitudForm
import hashlib
from django.views.decorators.csrf import csrf_exempt
import requests
import time

@login_required
def dashboard_view(request):
    role = getRole(request)
    if role == "AnalistaCredito":
        solicitudes = get_solicitudes()
        context = {
            'solicitudes_list': solicitudes
        }
        return render(request, 'ModuloFinanciero/solicitudes.html', context)
    elif role == "GerenteFinanciero":
        return render(request, 'ModuloFinanciero/gerente.html')
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
def report_view(request):
    role = getRole(request)
    if role == "GerenteFinanciero":
        #IP Microservicio
        t1 = time.time()
        sendEmail = requests.get('http://3.216.114.80:5000/getReport/')
        if sendEmail.status_code == 200:
            context = {
                'response': sendEmail.text,
                'time': time.time() - t1
            }
        return render(request, 'ModuloFinanciero/reporte.html', context)
    else:
        return HttpResponseForbidden()



@login_required
def solicitud_create(request):
    role = getRole(request)
    if role == "AnalistaCredito":
        if request.method == 'POST':
            form = SolicitudForm(request.POST)
            if form.is_valid():
                try:
                    concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaSolicitud").strftime("%Y-%m-%d") + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
                except (TypeError, AttributeError):
                    concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
                hash_object = hashlib.sha256(concat.encode()).hexdigest()
                if not hash_object == form.cleaned_data.get("hash"):
                    print("Different Hashes detected in create request!")
                    print("Received Hash: " + form.cleaned_data.get("hash"))
                    print("Calculated Hash: " + hash_object)
                    return HttpResponseForbidden()
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

@csrf_exempt
@login_required
def solicitud_create_csrf_exempt(request):
    role = getRole(request)
    if role == "AnalistaCredito":
        if request.method == 'POST':
            form = SolicitudForm(request.POST)
            if form.is_valid():
                try:
                    concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaSolicitud").strftime("%Y-%m-%d") + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
                except (TypeError, AttributeError):
                    concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
                hash_object = hashlib.sha256(concat.encode()).hexdigest()
                if not hash_object == form.cleaned_data.get("hash"):
                    print("Different Hashes detected in create request!")
                    print("Received Hash: " + form.cleaned_data.get("hash"))
                    print("Calculated Hash: " + hash_object)
                    return HttpResponseForbidden()
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

@csrf_exempt
def solicitud_create_insecure(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            try:
                concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaSolicitud").strftime("%Y-%m-%d") + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
            except (TypeError, AttributeError):
                concat = form.cleaned_data.get("estudiante") + form.cleaned_data.get("analista") + str(form.cleaned_data.get("montoAPagar")) + form.cleaned_data.get("fechaAprobacion").strftime("%Y-%m-%d")
            hash_object = hashlib.sha256(concat.encode()).hexdigest()
            if not hash_object == form.cleaned_data.get("hash"):
                print("Different Hashes detected in create request!")
                print("Received Hash: " + form.cleaned_data.get("hash"))
                print("Calculated Hash: " + hash_object)
                return HttpResponseForbidden()
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