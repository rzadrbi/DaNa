from random import randint
from sms_ir import SmsIr
from django.contrib.auth import login, authenticate, logout
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
    # TODO: 1- fix the sms verifi
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
            token = str(uuid4())
            sms_ir = SmsIr(
                api_key="vUkbNp2WIcXZkq6L9CnkhyoCyuAOIUbrlFlmEFutLcXsfYKXQAZtfmq1X4Daftzf",
                linenumber=30007732904886,
            )
            sms_ir.send_verify_code(
                number="+989133820954",
                template_id=244376,
                parameters=[{"name": "param", "value": rcode, }, ],
            )
            print(rcode)
            OTP.objects.create(token=token, random_code=rcode, phone=cd['phone'], password=cd['password'],
                               fullname=cd['fullname'])
            return redirect(reverse("account:otp") + f'?token={token}')
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
            if OTP.objects.filter(token=token, random_code=cd['randcode']).exists():
                userotp = OTP.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=userotp.phone, password=userotp.password,
                                                             fullname=userotp.fullname)
                login(request, user)
                userotp.delete()
                return redirect(reverse("Home:main"))
        message = 'Registration failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


def signout(request):
    logout(request)
    return redirect('Home:main')
