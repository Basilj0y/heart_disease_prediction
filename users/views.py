from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
import string

# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            dob = form.cleaned_data.get('dob')
            hospital_name = form.cleaned_data.get('hospital_name')
            profile = UserProfile(user=user, phone_number=phone_number, dob=dob, hospital_name=hospital_name)
            profile.save()
            login(request, user)

            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):  # don't name it 'login' because Django already has a built-in login function
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('successfully_logged_in') 
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required  
def successfully_logged_in(request):
    return render(request, 'users/successfully_logged_in.html')



def generate_otp():
    return ''.join(random.choices(string.digits, k=6))



def send_otp_email(user_email, otp):
    send_mail(
        'Password Reset OTP',
        f'Your OTP for password reset is {otp}.',
        '', 
        [user_email],
        fail_silently=False,
    )


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()  
            
            
            request.session['otp'] = otp
            request.session['email'] = email

            
            send_otp_email(email, otp)

            return redirect('verify_otp')  
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email not found!'})
    return render(request, 'users/forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if otp_input == request.session.get('otp'):
            
            return redirect('reset_password')  
        else:
            return render(request, 'users/verify_otp.html', {'error': 'Invalid OTP!'})

    return render(request, 'users/verify_otp.html')


def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        email = request.session.get('email')
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)  
            user.save()

            
            login(request, user)

            return redirect('login')  
        except User.DoesNotExist:
            return redirect('login')  
    return render(request, 'users/reset_password.html')

from django.shortcuts import render

def view_patients(request):
    # Logic to fetch and display patients
    return render(request, 'health/view_patients.html')  # Or whatever template you use




from sklearn.preprocessing import StandardScaler


from sklearn.preprocessing import OneHotEncoder
import joblib 


from sklearn.preprocessing import LabelEncoder

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import pickle
from .forms import Health_Prediction_form

# Load your trained models

label_encoder = joblib.load('./label_encoder.pkl')
train_column=joblib.load('./train_columns.pkl')
scaler = joblib.load('scaler.pkl')
#knn_model=joblib.load('./hdp_model_pipeline.pkl')
knn_model=joblib.load('knn_model.pkl')
def patient_form(request):
    if request.method == 'POST':
        form = Health_Prediction_form(request.POST)
        if form.is_valid():
            # Capture the form data
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            temperature = form.cleaned_data['temperature']
            heart_rate = form.cleaned_data['heart_rate']
            cholestrol = form.cleaned_data['cholestrol']
            blood_sugar = form.cleaned_data['blood_sugar']
            systolic = form.cleaned_data['systolic']
            diastolic = form.cleaned_data['diastolic']
            existing_conditions = form.cleaned_data['existing_conditions']
            family_history = form.cleaned_data['family_history']
            smoking_status = form.cleaned_data['smoking_status']
            lab_status = form.cleaned_data['lab_status']
            symptoms = form.cleaned_data['symptom']  
           

            
            User_data = {
                "Height_cm": height,
                "Weight_kg": weight,
                "Temperature_C": temperature,
                "Heart_Rate": heart_rate,
                "Cholesterol_mg_dL": cholestrol,
                "Blood_Sugar_mg_dL": blood_sugar,
                "Systolic_BP": systolic,
                "Diastolic_BP": diastolic,
                "Symptoms": symptoms,  
                "Existing_Conditions": existing_conditions,
                "Laboratory_Test_Results": lab_status,
                "Smoking_Status": smoking_status,
                "Family_History_Heart_Disease": family_history
            }
            input_df=pd.DataFrame([User_data])
         
            categorical_columns = [
                "Symptoms",
                "Existing_Conditions",
                "Laboratory_Test_Results",
                "Smoking_Status",
                "Family_History_Heart_Disease"
                ]
            input_df=pd.get_dummies(input_df, columns=categorical_columns)
            
            
            # Ensure all required columns are present, adding missing ones with value 0
            for col in train_column:
                if col not in input_df.columns:
                    input_df[col] = False  # Add missing columns with value 0
            input_df=input_df[train_column]
            # Reorder columns to match the model's expected order
            
            # Prediction
            scaled_input = scaler.transform(input_df.values)
            prediction = knn_model.predict(scaled_input)
            
            decoded_prediction = label_encoder.inverse_transform(prediction)
            request.session['prediction'] = ', '.join(decoded_prediction)
            return redirect('predict_health')  
        else:
            return JsonResponse({'error': 'Invalid form input'}, status=400)

    else:
        form = Health_Prediction_form()
        return render(request, 'health/patient_form.html', {'form': form})


from django.shortcuts import render
from django.http import HttpResponse
def predict_health(request):
    
    prediction = request.session.get('prediction', 'No prediction available')
    return render(request, 'health/prediction_result.html', {'prediction': prediction})