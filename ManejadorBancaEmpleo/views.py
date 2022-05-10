from time import sleep
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from django.shortcuts import render
from .serializers import JobListingSerializer, EmpresaSerializer, SolicitudEmpleoSerializer
from django.http.response import JsonResponse
from .logic import job_listings_logic as jbl
from rest_framework import status
from rest_framework.parsers import JSONParser 
import random
import time


def jobListing_list(request):
    if request.method == 'GET':
        eleccion = random.choice(["TIMEOUT","FALLO","NORMAL"])
        if eleccion == "NORMAL":
            jobListings = jbl.get_job_listings()
            jl_serializer = JobListingSerializer(jobListings, many=True)
            return JsonResponse(jl_serializer.data, safe=False)
        elif eleccion == "FALLO":
           return HttpResponseServerError()
        else:
            time.sleep(random.randint(5,10))
            return HttpResponse(status = 408)

def jobListing_get_by_major(request, major):
    if request.method == 'GET':
        jobListings = jbl.get_job_listing_by_major(major)
        jl_serializer = JobListingSerializer(jobListings, many=True)
        return JsonResponse(jl_serializer.data, safe=False)

def job_listing_create(request):
    if request.method == 'POST':
        jl_dto = JSONParser().parse(request)
        jd_serializer = JobListingSerializer(data=jl_dto)
        if jd_serializer.is_valid():
            jd_serializer.save()
            return JsonResponse(jd_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(jd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest()

def empresa_create(request):
    if request.method == 'POST':
        emp_dto = JSONParser().parse(request)
        emp_serializer = EmpresaSerializer(data=emp_dto)
        if emp_serializer.is_valid():
            emp_serializer.save()
            return JsonResponse(emp_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest()

def solicitudEmpleo_create(request):
    if request.method == 'POST':
        se_dto = JSONParser().parse(request)
        se_serializer = SolicitudEmpleoSerializer(data=se_dto)
        if se_serializer.is_valid():
            se_serializer.save()
            return JsonResponse(se_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(se_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponseBadRequest()