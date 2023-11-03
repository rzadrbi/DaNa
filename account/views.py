from random import randint

from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, CreateView
from account.forms import LoginForm, RegisterForm, OTPform
from account.models import User, OTP
from uuid import uuid4

class LoginPageView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home:main')
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                phone=form.cleaned_data['phone'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('Home:main')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})



class Register(View):
    template_name = 'register.html'
    form_class = RegisterForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home:main')
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rcode = randint(1000, 9999)
            token = uuid4()
            OTP.objects.create(token=token, random_code=rcode, phone=cd['phone'], password=cd['password'], fullname=cd['fullname'])
            return redirect(reverse("account:otp") + f'?token={cd[token]}')
        message = 'Registration failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


class OTPview(View):
    template_name = 'OTP.html'
    form_class = OTPform

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home:main')
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        token = request.GET.get('token')
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            OTP.objects.create(token=token, random_code=rcode, phone=cd['phone'], password=cd['password'],
                               fullname=cd['fullname'])
            return redirect("Home:main")
        message = 'Registration failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})