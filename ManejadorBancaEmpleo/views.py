from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from .serializers import JobListingSerializer
from django.http.response import JsonResponse
from .logic import job_listings_logic as jbl
from rest_framework import status
from rest_framework.parsers import JSONParser 

def jobListing_list(request):
    if request.method == 'GET':
        jobListings = jbl.get_job_listings()
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