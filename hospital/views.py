
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import HospitalRegistrationForm
from .models import Hospital, Department

# def hospital_register(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = HospitalRegistrationForm(request.POST)
#         if form.is_valid():
#             # Create user
#             user = form.save()
#             print(user)
            
#             # Create hospital
#             hospital = Hospital.objects.create(
#                 user=user,
#                 name=form.cleaned_data['name'],
#                 registration_id=form.cleaned_data['registration_id'],
#                 phone=form.cleaned_data['phone'],
#                 emergency_phone=form.cleaned_data['emergency_phone'],
#                 email=form.cleaned_data['email'],
#                 website=form.cleaned_data['website'],
#                 address=form.cleaned_data['address'],
#                 latitude=form.cleaned_data.get('latitude'),
#                 longitude=form.cleaned_data.get('longitude'),
#                 city=form.cleaned_data['city'],
#                 state=form.cleaned_data['state'],
#                 pincode=form.cleaned_data['pincode'],
#                 established_date=form.cleaned_data['established_date'],
#                 description=form.cleaned_data['description'],
#                 facilities=form.cleaned_data['facilities']
#             )
            
#             # Create departments
#             for dept_code in form.cleaned_data['departments']:
#                 Department.objects.create(
#                     hospital=hospital,
#                     department_type=dept_code,
#                     total_beds=0,  # Will be updated later
#                     available_beds=0
#                 )
            
#             login(request, user)
#             return redirect('home')
#     else:
#         form = HospitalRegistrationForm()
    
#     return render(request, 'hospital/register.html', {
#         'form': form,
#         'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'
#     })

def hospital_register(request):
    if request.method == 'POST':
        print("\n=== RAW POST DATA ===")
        print(request.POST)
        
        form = HospitalRegistrationForm(request.POST)
        print("\n=== FORM VALIDATION ===")
        print("Is valid?", form.is_valid())
        print("Errors:", form.errors)
        
        if form.is_valid():
            print("\n=== CLEANED DATA ===")
            print(form.cleaned_data)
            
            try:
                # User creation
                user = form.save()
                print("\n=== USER CREATED ===")
                print(f"Username: {user.username}, ID: {user.pk}")
                
                # Hospital creation
                hospital_data = {
                    'user': user,
                    'name': form.cleaned_data['name'],
                    'registration_id': form.cleaned_data['registration_id'],
                    'phone': form.cleaned_data['phone'],
                    'emergency_phone': form.cleaned_data['emergency_phone'],
                    'email': form.cleaned_data['email'],
                    'website': form.cleaned_data['website'],
                    'address': form.cleaned_data['address'],
                    'latitude': form.cleaned_data.get('latitude'),
                    'longitude': form.cleaned_data.get('longitude'),
                    'city': form.cleaned_data['city'],
                    'state': form.cleaned_data['state'],
                    'pincode': form.cleaned_data['pincode'],
                    'established_date': form.cleaned_data['established_date'],
                    'description': form.cleaned_data['description'],
                    'facilities': form.cleaned_data['facilities']
                }
                
                print("\n=== HOSPITAL DATA ===")
                print(hospital_data)
                
                hospital = Hospital.objects.create(**hospital_data)
                print(f"Hospital created: ID {hospital.pk}")
                
                # Department creation
                print("\n=== DEPARTMENTS ===")
                for dept_code in form.cleaned_data['departments']:
                    dept = Department.objects.create(
                        hospital=hospital,
                        department_type=dept_code,
                        total_beds=0,
                        available_beds=0
                    )
                    print(f"Created {dept.get_department_type_display()} department")
                
                login(request, user)
                print("\n=== REDIRECTING ===")
                return redirect('home')
                
            except Exception as e:
                print("\n=== EXCEPTION ===")
                print(str(e))
                raise
    else:
        form = HospitalRegistrationForm()
    
    return render(request, 'hospital/register.html', {
        'form': form,
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'
    })


def home(request):
    return render(request, 'hospital/hospital_home.html')
