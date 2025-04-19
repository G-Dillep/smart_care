from django import forms
from .models import Doctor

class DoctorRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = [  # all fields except confirm_password
            'full_name', 'gender', 'dob', 'profile_photo',
            'email', 'phone', 'alternate_phone', 'address', 'city', 'state', 'pincode',
            'specialization', 'experience', 'license_number', 'medical_council',
            'qualifications', 'hospital_clinic', 'working_days', 'working_hours',
            'consultation_fee', 'username', 'password',
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
