from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    dob = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))
    hospital_name = forms.CharField(required=True, max_length=100)
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'dob', 'hospital_name', 'password1', 'password2']
