from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
# Create your views here.

def dashboard_view(request):
    if not request.user.is_authenticated:
        response = redirect('accounts/login/')
        return response
    if not request.user.groups.filter(name='AnalistaCredito').exists():
        return HttpResponseForbidden()

    return render(request, 'dashboard.html')