from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Hospital, Department
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
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
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital Name'}),
        label=_("Hospital Name"),
        help_text=_("Official name of your hospital")
    )
    
    registration_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("License Number"),
        help_text=_("Government issued license number")
    )

    # Step 2: Contact Info
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91XXXXXXXXXX'}),
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', _("Enter a valid phone number"))]
    )
    
    emergency_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', _("Enter a valid phone number"))]
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text=_("Official email address")
    )
    
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
        help_text=_("Optional hospital website")
    )

    # Step 3: Location Info
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text=_("Full physical address")
    )
    
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^\d{6}$', _("Enter a valid 6-digit pincode"))]
    )
    
    latitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    longitude = forms.FloatField(
        widget=forms.HiddenInput(),
        required=False
    )

    # Step 4: Departments
    departments = forms.MultipleChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text=_("Select all available departments")
    )

    # Step 5: Additional Info
    established_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text=_("Date when hospital was established")
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text=_("Brief description about your hospital")
    )
    
    facilities = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text=_("List of special facilities available")
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'username': _("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize password help text
        self.fields['password1'].help_text = _(
            "Your password must contain at least 8 characters."
        )
        self.fields['password2'].help_text = _(
            "Enter the same password as before, for verification."
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email address is already in use."))
        return email

    def clean_registration_id(self):
        reg_id = self.cleaned_data.get('registration_id')
        if Hospital.objects.filter(registration_id=reg_id).exists():
            raise ValidationError(_("A hospital with this license number already exists."))
        return reg_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user