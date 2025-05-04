from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Hospital, Department
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email

DEPARTMENT_CHOICES = [
    ('ER', 'Emergency'),
    ('ICU', 'Intensive Care Unit'),
    ('CAR', 'Cardiology'),
    ('NEU', 'Neurology'),
    ('PED', 'Pediatrics'),
    ('ORT', 'Orthopedics'),
    ('GEN', 'General Medicine'),
]

class HospitalRegistrationForm(UserCreationForm):
    # Step 1: Basic Info
    name = forms.CharField(max_length=200, required=True)
    registration_id = forms.CharField(max_length=50, required=True)
    
    # Step 2: Contact Info
    phone = forms.CharField(max_length=15, required=True)
    emergency_phone = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=True)
    website = forms.URLField(required=False)
    
    # Step 3: Location Info
    address = forms.CharField(widget=forms.Textarea, required=True)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    
    # Step 4: Departments
    departments = forms.MultipleChoiceField(
        choices=Department.DEPARTMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    # Step 5: Additional Info
    established_date = forms.DateField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    facilities = forms.CharField(widget=forms.Textarea, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_registration_id(self):
        reg_id = self.cleaned_data.get('registration_id')
        if Hospital.objects.filter(registration_id=reg_id).exists():
            raise ValidationError("A hospital with this license number already exists.")
        return reg_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class HospitalLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            validate_email(username)
            return username
        except ValidationError:
            return username