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
