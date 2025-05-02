from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DoctorRegistrationForm
from .models import Doctor
from django.contrib import messages


def home(request):
    return render(request, 'doctor/doctor_home.html')

#=================================================================================================
#Doctor registration
#=================================================================================================

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
            return redirect('doctor_details')
    else:
        print("Request method is GET")
        print("Request data:", request.GET)
        form = DoctorRegistrationForm()
    return render(request, 'doctor/register.html', {'form': form})


def doctor_details(request):
    # Fetch the doctor based on the ID from the database
    doctors = Doctor.objects.all()
    return render(request, 'doctor/doctor_details.html', {'doctors': doctors})
#=================================================================================================


#=================================================================================================
#Doctor Login
#=================================================================================================
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Both username and password are required")
            return render(request, 'doctor/doctor_login.html', 
                        {'username_value': username})
        
        try:
            doctor = Doctor.objects.get(username=username)
            if doctor.password == password:
                request.session['doctor_id'] = doctor.id
                request.session.set_expiry(3600)
                return redirect('doctor_dashboard')
            messages.error(request, "Incorrect password")
        except Doctor.DoesNotExist:
            messages.error(request, "Username not found")

        return render(request, 'doctor/doctor_login.html', 
                    {'username_value': username})

    return render(request, 'doctor/doctor_login.html')

def doctor_dashboard(request):
    if 'doctor_id' not in request.session:
        messages.error(request, "Please login first")
        return redirect('doctor_login')
    
    try:
        doctor = Doctor.objects.get(id=request.session['doctor_id'])
        return render(request, 'doctor/doctor_dashboard.html', {'doctor': doctor})
    except Doctor.DoesNotExist:
        messages.error(request, "Session expired")
        request.session.flush()
        return redirect('doctor_login')

def doctor_logout(request):
    request.session.flush()
    return redirect('doctor_login')

#=================================================================================================


#=================================================================================================
#Doctor Profile
#=================================================================================================



