from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('successfully_logged_in/', views.successfully_logged_in, name='successfully_logged_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),  
    path('verify_otp/', views.verify_otp, name='verify_otp'),  
    path('reset_password/', views.reset_password, name='reset_password'),  
]
