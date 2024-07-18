import email
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            email=self.normalize_email(phone),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="ایمیل",
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )
    fullname = models.CharField(max_length=50, verbose_name='نام کامل')
    phone = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class OTP(models.Model):
    token = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    random_code = models.IntegerField()


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('user'))
    full_name = models.CharField(max_length=100, verbose_name=_('full_name'))
    email = models.EmailField(max_length=100, verbose_name=_('email'))
    phone = models.CharField(max_length=11, verbose_name=_('phone_number'))
    address = models.TextField(max_length=500, verbose_name=_('address'))
    postal_code = models.CharField(max_length=100, verbose_name=_('postal_code'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.user.phone


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('your name'))
    email = models.EmailField(max_length=100, verbose_name=_('your email'))
    phone = models.CharField(max_length=11, verbose_name=_('your phone'))
    subject = models.CharField(max_length=100, verbose_name=_('subject'))
    message = models.TextField(max_length=500, verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = _('contact us')
        verbose_name_plural = _('contact us')

    def __str__(self):
        return self.name
