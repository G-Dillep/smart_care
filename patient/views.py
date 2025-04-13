from django.shortcuts import render
from django.http import HttpResponse
def home(request):
    return render(request, 'patient/patient_home.html')