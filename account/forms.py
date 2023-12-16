from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
import re
from django.core.exceptions import ValidationError

from account.models import User, Address


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="گذرواژه", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار گذرواژه", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone", ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "is_active", "is_admin", ]


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل'}),
                            validators=[validators.MaxLengthValidator(11)])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'گذرواژه'}))

    def clean_password(self):
        phn = self.cleaned_data.get('phone')
        psw = self.cleaned_data.get('password')
        if authenticate(username=phn, password=psw) is None:
            raise ValidationError('شماره موبایل یا رمز عبور اشتباه است', code='uop_wrong')
        return self.cleaned_data.get('password')

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not re.findall("^09", phone):
            raise ValidationError("شماره موبایل باید با 09 شروع شود !", code="not_phone")
        return phone


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=11,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل'}),
                            validators=[validators.MaxLengthValidator(11)])
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'گذرواژه'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار گذرواژه'}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه ها برابر نیستند !", code= 'not_same_pass')
        if len(password1) < 8:
            raise ValidationError('طول گذرواژه نباید کمتر از ۸ کاراکتر باشد !', code='pass_len')
        if str(password1).isnumeric() or not bool(re.search("\d", password1)):
            raise ValidationError('گذرواژه باید ترکیبی از عدد و حرف باشد !', code='pass_len')
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not re.findall("^09", phone):
            raise ValidationError("شماره موبایل باید با 09 شروع شود !", code="not_phone")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError('این شماره موبایل دارای پروفایل کاربری میباشد!', code='phone_exists')
        if not str(phone).isnumeric():
            raise ValidationError('شماره موبایل باید از عدد تشکیل شده باشد !', code='phone_exists')
        return phone


class OTPform(forms.Form):
    randcode = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تایید ارسال شده به شماره موبایل خود را وارد کنید'}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

