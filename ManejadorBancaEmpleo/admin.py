from django.contrib import admin

from ManejadorBancaEmpleo.models import JobListing, Empresa, SolicitudesEmpleo

admin.site.register(JobListing)
admin.site.register(Empresa)
admin.site.register(SolicitudesEmpleo)

