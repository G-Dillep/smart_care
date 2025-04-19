from django.db import models


class Doctor(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()
    profile_photo = models.ImageField(upload_to='doctor/static/doctor/Registered_doctor_profiles/', blank=True, null=True)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    license_number = models.CharField(max_length=100, unique=True)
    medical_council = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=255)
    hospital_clinic = models.CharField(max_length=255)
    working_days = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=100)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Hash later in form or view

    def __str__(self):
        return self.full_name
