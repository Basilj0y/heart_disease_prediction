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
        
   

class Health_Prediction_form(forms.Form):     
        
        height = forms.FloatField(
        label='Height (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        weight = forms.FloatField(
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        temperature = forms.FloatField(
        label='Temperature (C)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        heart_rate = forms.FloatField(
        label='Heart_rate (C)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        cholestrol = forms.FloatField(
        label='Cholestrol (mg/dl)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        blood_sugar = forms.FloatField(
        label='Blood_Sugar  (mg/dl)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        systolic = forms.FloatField(
        label='Systolic Pressure',
       widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        diastolic = forms.FloatField(
        label='Diastolic Pressure',        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        existing_conditions = forms.ChoiceField(
        choices=[
            ('Diabetes', 'Diabetes'),
            ('Hypertension', 'Hypertension'),
            ('High Cholesterol', 'High Cholesterol'),
            ('Asthma', 'Asthma'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        family_history = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        label='Family History of Heart Disease',
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        smoking_status = forms.ChoiceField(
        choices=[
            ('Never', 'Never'),
            ('Former', 'Former'),
            ('Current', 'Current'),
    
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        lab_status = forms.ChoiceField(
        choices=[
            ('High Blood Sugar', 'High Blood Sugar'),
            ('High Cholesterol', 'High Cholesterol'),
            ('Low Iron', 'Low Iron'),
            ('Normal Test Results', 'Normal Test Results'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        symptom= forms.ChoiceField(
        choices=[
            ('chest pain', 'chest pain'),
            ('dizziness', 'dizziness'),
            ('fatigue', 'fatigue'),
            ('nausea', 'nausea'),
            ('palpitations', 'palpitations'),
            ('shortness of breath', 'shortness of breath'),

        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        
 