
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import HospitalRegistrationForm, HospitalLoginForm
from .models import Hospital, Department
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.middleware.csrf import get_token
import pprint


def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = form.save()
                
                # Create hospital
                hospital = Hospital.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    registration_id=form.cleaned_data['registration_id'],
                    phone=form.cleaned_data['phone'],
                    emergency_phone=form.cleaned_data['emergency_phone'],
                    email=form.cleaned_data['email'],
                    website=form.cleaned_data['website'],
                    address=form.cleaned_data['address'],
                    latitude=form.cleaned_data.get('latitude'),
                    longitude=form.cleaned_data.get('longitude'),
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    pincode=form.cleaned_data['pincode'],
                    established_date=form.cleaned_data['established_date'],
                    description=form.cleaned_data['description'],
                    facilities=form.cleaned_data['facilities']
                )
                
                # Create departments with bed counts
                for dept_code in form.cleaned_data['departments']:
                    total_beds = request.POST.get(f'{dept_code}_total', 0) or 0
                    available_beds = request.POST.get(f'{dept_code}_available', 0) or 0
                    
                    Department.objects.create(
                        hospital=hospital,
                        department_type=dept_code,
                        total_beds=total_beds,
                        available_beds=available_beds
                    )
                
                login(request, user)
                return redirect('hospital_dashboard')
                
            except Exception as e:
                # Handle any exceptions during creation
                form.add_error(None, f"An error occurred: {str(e)}")
        else:
            # Form is invalid, errors will be displayed in template
            pass
    else:
        form = HospitalRegistrationForm()
    
    return render(request, 'hospital/register.html', {
        'form': form,
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'
    })

@csrf_protect
def hospital_login(request):
    if request.user.is_authenticated:
        return redirect('hospital_dashboard')
    
    if request.method == 'POST':
        form = HospitalLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = form.get_user()  # This is the proper way to get authenticated user
            
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            
            try:
                hospital = user.hospital
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('hospital_dashboard'),
                        'message': f'Welcome back, {hospital.name}!'
                    })
                messages.success(request, f'Welcome back, {hospital.name}!')
                return redirect('hospital_dashboard')
            
            except AttributeError:
                logout(request)
                error_msg = 'This account is not associated with a hospital.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    }, status=400)
                messages.error(request, error_msg)
                return redirect('hospital_login')
        
        # Form is invalid
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            }, status=400)
        
        return render(request, 'hospital/login.html', {'form': form})
    
    else:
        form = HospitalLoginForm()
    
    return render(request, 'hospital/login.html', {'form': form})

def hospital_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('hospital_login')

def hospital_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('hospital_login')
    
    try:
        hospital = request.user.hospital
    except AttributeError:
        messages.error(request, 'This account is not associated with a hospital.')
        return redirect('hospital_login')
    
    context = {
        'hospital': hospital,
        'departments': hospital.departments.all()
    }
    return render(request, 'hospital/dashboard.html', context)






def home(request):
    return render(request, 'hospital/hospital_home.html')
