from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from EducacionEstrella.auth0backend import getRole
# Create your views here.

@login_required
def dashboard_view(request):
    role = getRole(request)
    #TODO Set what happens after
    if role == "AnalistaCredito":
        return render(request, 'dashboard.html')
    else:
        return HttpResponseForbidden()
