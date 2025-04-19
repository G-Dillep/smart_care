from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorRegistrationForm
from .models import Doctor

def home(request):
    return render(request, 'doctor/doctor_home.html')




def register_doctor(request):
    if request.method == 'POST':
        print("Request method is POST")
        print("Request data:", request.POST)
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            print("Form data:", form.cleaned_data)
            doctor = form.save(commit=False)
            # Optional: Hash password here
            doctor.save()
            return redirect('doctor/doctors')  # or redirect to 'doctor_list' to verify
    else:
        print("Request method is GET")
        print("Request data:", request.GET)
        form = DoctorRegistrationForm()
    return render(request, 'doctor/register.html', {'form': form})


def doctor_details(request):
    # Fetch the doctor based on the ID from the database
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_details.html', {'doctors': doctors})


