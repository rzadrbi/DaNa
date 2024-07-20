from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginPageView.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('OTP', views.OTPview.as_view(), name='otp'),
    path('logout', views.signout, name='signout'),
    path('create_address', views.AddressView.as_view(), name='add_address_view'),
    path('update_address', views.Update_Address, name='update_address_view'),
    path('my_account', views.my_account.as_view(), name='my_account'),
]
