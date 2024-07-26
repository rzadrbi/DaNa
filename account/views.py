from random import randint
from sms_ir import SmsIr
from django.contrib.auth import login, authenticate, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View, CreateView, UpdateView, TemplateView
from account.forms import LoginForm, RegisterForm, OTPform, AddressForm, contactusForm
from account.models import User, OTP, Address
from uuid import uuid4

from cart.models import DiscountCode, Order


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
                next_page = request.GET.get('next')
                if next_page is not None:
                    return redirect(next_page)
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
                number=f"{cd['phone']}",
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


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('Home:main')
        return render(request, 'add_address.html', {'form': form})


def Update_Address(request):
    address = get_object_or_404(Address, user=request.user)
    if request.method == 'POST':
        form = AddressForm(data=request.POST)
        if form.is_valid():
            address.full_name = form.cleaned_data['full_name']
            address.email = form.cleaned_data['email']
            address.phone = form.cleaned_data['phone']
            address.address = form.cleaned_data['address']
            address.postal_code = form.cleaned_data['postal_code']
            address.save()
            return redirect('Home:main')
    else:
        form = AddressForm
    return render(request, 'add_address.html', {'form': form, })


# def my_account(request):
#     return render(request, 'my_account.html', {})

class my_account(View):
    template_name = 'my_account.html'

    def get(self, request):
        return render(request, self.template_name, )


class contact_us(View):
    template_name = 'contact_us.html'

    def get(self, request):
        form = contactusForm
        return render(request, self.template_name, {'form': form, })
