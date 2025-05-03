from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    VERIFICATION_STATUS = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ]
    
    # Core Details
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    registration_id = models.CharField(max_length=50, unique=True)
    verification_status = models.CharField(max_length=1, choices=VERIFICATION_STATUS, default='P')
    
    # Contact
    phone = models.CharField(max_length=15)
    emergency_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Location
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)  # Temporary storage
    longitude = models.FloatField(null=True, blank=True) # Temporary storage
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Meta
    established_date = models.DateField()
    description = models.TextField(blank=True)
    facilities = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('ER', 'Emergency'),
        ('ICU', 'Intensive Care Unit'),
        ('CAR', 'Cardiology'),
        ('NEU', 'Neurology'),
        ('PED', 'Pediatrics'),
        ('ORT', 'Orthopedics'),
        ('GEN', 'General Medicine'),
        ('SUR', 'Surgery'),
        ('ONC', 'Oncology'),
        ('GYN', 'Gynecology'),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    department_type = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    total_beds = models.PositiveIntegerField()
    available_beds = models.PositiveIntegerField()
    incharge = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.get_department_type_display()} ({self.hospital.name})"