from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginPageView.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('OTP', views.OTPview.as_view(), name='otp'),
    path('logout', views.signout, name='signout'),
]
