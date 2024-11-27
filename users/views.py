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
        'your_email@example.com', 
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


import numpy as np
from sklearn.preprocessing import OneHotEncoder
import joblib 


from sklearn.preprocessing import LabelEncoder

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import pickle
from .forms import Health_Prediction_form

# Load your trained models
with open(r'E:\heart_disease_prediction\heart_disease_prediction\knn_model.pkl', 'rb') as model_file:
    model1 = pickle.load(model_file)

with open(r'E:\heart_disease_prediction\heart_disease_prediction\scaler.pkl', 'rb') as scaler_file:
    scaler1 = pickle.load(scaler_file)

#with open(r'E:\heart_disease_prediction\heart_disease_prediction\encoder.pkl', 'rb') as encoder_file:
 #   one_hot_encoder = pickle.load(encoder_file)

with open(r'E:\heart_disease_prediction\heart_disease_prediction\label_encoder.pkl', 'rb') as label_encoder_file:
    label_encoder = pickle.load(label_encoder_file)

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
            # Creating a dictionary for categorical columns and initializing all as False
            categorical_columns = [
                'Symptoms_chest pain', 'Symptoms_dizziness', 'Symptoms_fatigue', 
                'Symptoms_nausea', 'Symptoms_palpitations', 'Symptoms_shortness of breath',
                'Existing_Conditions_Asthma', 'Existing_Conditions_Diabetes', 
                'Existing_Conditions_High Cholesterol', 'Existing_Conditions_Hypertension', 
                'Existing_Conditions_Thyroid', 'Laboratory_Test_Results_High Blood Sugar', 
                'Laboratory_Test_Results_High Cholesterol', 'Laboratory_Test_Results_Low Iron', 
                'Laboratory_Test_Results_Normal', 'Smoking_Status_Current', 
                'Smoking_Status_Former', 'Smoking_Status_Never', 
                'Family_History_Heart_Disease_No', 'Family_History_Heart_Disease_Yes'
            ]
            
            # Initialize all columns to False
            input_data = {col: [False] for col in categorical_columns}
            
            # Set the appropriate columns to True based on user selection
            if 'chest pain' in symptoms:
                input_data['Symptoms_chest pain'] = [True]
            if 'dizziness' in symptoms:
                input_data['Symptoms_dizziness'] = [True]
            if 'fatigue' in symptoms:
                input_data['Symptoms_fatigue'] = [True]
            if 'nausea' in symptoms:
                input_data['Symptoms_nausea'] = [True]
            if 'palpitations' in symptoms:
                input_data['Symptoms_palpitations'] = [True]
            if 'shortness of breath' in symptoms:
                input_data['Symptoms_shortness of breath'] = [True]
            
            if 'Asthma' in existing_conditions:
                input_data['Existing_Conditions_Asthma'] = [True]
            if 'Diabetes' in existing_conditions:
                input_data['Existing_Conditions_Diabetes'] = [True]
            if 'High Cholesterol' in existing_conditions:
                input_data['Existing_Conditions_High Cholesterol'] = [True]
            if 'Hypertension' in existing_conditions:
                input_data['Existing_Conditions_Hypertension'] = [True]
            if 'Thyroid' in existing_conditions:
                input_data['Existing_Conditions_Thyroid'] = [True]
            
            if 'High Blood Sugar' in lab_status:
                input_data['Laboratory_Test_Results_High Blood Sugar'] = [True]
            if 'High Cholesterol' in lab_status:
                input_data['Laboratory_Test_Results_High Cholesterol'] = [True]
            if 'Low Iron' in lab_status:
                input_data['Laboratory_Test_Results_Low Iron'] = [True]
            if 'Normal' in lab_status:
                input_data['Laboratory_Test_Results_Normal'] = [True]
            
            if smoking_status == 'Current':
                input_data['Smoking_Status_Current'] = [True]
            if smoking_status == 'Former':
                input_data['Smoking_Status_Former'] = [True]
            if smoking_status == 'Never':
                input_data['Smoking_Status_Never'] = [True]
            
            if family_history == 'Yes':
                input_data['Family_History_Heart_Disease_Yes'] = [True]
            else:
                input_data['Family_History_Heart_Disease_No'] = [True]
            
            # Add other continuous fields
            input_data['Height_cm'] = [height]
            input_data['Weight_kg'] = [weight]
            input_data['Temperature_C'] = [temperature]
            input_data['Heart_Rate'] = [heart_rate]
            input_data['Cholesterol_mg_dL'] = [cholestrol]
            input_data['Blood_Sugar_mg_dL'] = [blood_sugar]
            input_data['Systolic_BP'] = [systolic]
            input_data['Diastolic_BP'] = [diastolic]
            
            # Create DataFrame for the input data
            input_df= pd.DataFrame(input_data)
            
            # Define the exact column order from the training data
            model_columns = [
                'Height_cm', 'Weight_kg', 'Temperature_C', 'Heart_Rate', 'Cholesterol_mg_dL', 
                'Blood_Sugar_mg_dL', 'Symptoms_chest pain', 'Symptoms_dizziness', 'Symptoms_fatigue', 
                'Symptoms_nausea', 'Symptoms_palpitations', 'Symptoms_shortness of breath',
                'Existing_Conditions_Asthma', 'Existing_Conditions_Diabetes', 
                'Existing_Conditions_High Cholesterol', 'Existing_Conditions_Hypertension', 
                'Existing_Conditions_Thyroid', 'Laboratory_Test_Results_High Blood Sugar', 
                'Laboratory_Test_Results_High Cholesterol', 'Laboratory_Test_Results_Low Iron', 
                'Laboratory_Test_Results_Normal', 'Smoking_Status_Current', 
                'Smoking_Status_Former', 'Smoking_Status_Never', 
                'Family_History_Heart_Disease_No', 'Family_History_Heart_Disease_Yes', 
                'Systolic_BP', 'Diastolic_BP'
            ]
            
            # Ensure all required columns are present, adding missing ones with value 0
            for col in model_columns:
                if col not in input_df.columns:
                    input_df[col] = 0  # Add missing columns with value 0
            
            # Reorder columns to match the model's expected order
            input_df = input_df[model_columns]
            #input_df.to_csv('input_df.csv', index=False)
            #input_df=pd.read_csv('input_df.csv')
            #input_df= input_df.values.reshape(-1, 1)

            #input_scaled = scaler1.transform(input_df)

            # Prediction
            prediction = model1.predict(input_df)
            #decoded_prediction = label_encoder.inverse_transform([int(prediction[0])])[0]
            # Return the prediction result as JSON response
            return JsonResponse({'prediction': int(prediction[0])})


        else:
            return JsonResponse({'error': 'Invalid form input'}, status=400)

    else:
        form = Health_Prediction_form()
        return render(request, 'health/patient_form.html', {'form': form})


from django.shortcuts import render
from django.http import HttpResponse
def predict_health(request):
    
    return HttpResponse("Prediction result")