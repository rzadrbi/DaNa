from django.db import models


class contact_phone(models.Model):
    phone = models.CharField(max_length=11, verbose_name='شماره ارتباط با ما')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'شماره تماس'
        verbose_name_plural = 'شماره های تماس'


class sample(models.Model):
    pass




