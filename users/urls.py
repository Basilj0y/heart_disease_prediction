from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('successfully_logged_in/', views.successfully_logged_in, name='successfully_logged_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),  
    path('verify_otp/', views.verify_otp, name='verify_otp'),  
    path('reset_password/', views.reset_password, name='reset_password'),
    path('predict_health/', views.predict_health, name='predict_health'),
    path('patient-form/', views.patient_form, name='patient_form'),
    path('view-patients/', views.view_patients, name='view_patients'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
