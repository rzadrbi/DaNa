import uuid

import shortuuid
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify
from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.TimeField(auto_now_add=True, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Color(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.TimeField(auto_now_add=True, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'


class Size(models.Model):
    title = models.CharField(max_length=100, unique=True, )
    created_at = models.TimeField(auto_now_add=True, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.TimeField(auto_now_add=True, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'


class Product(models.Model):
    title = models.CharField(max_length=100)
    cate = models.ManyToManyField(Category, related_name='categories')
    description = models.TextField()
    information = models.TextField()
    slug = models.SlugField(blank=True, unique=True, verbose_name='اسلاگ')
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, related_name='company', blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='colors')
    size = models.ManyToManyField(Size, blank=True, null=True, related_name='sizes')
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.title} --- {self.price}'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_absolute_url(self):  # TODO: set url
        return reverse('', args=[self.slug])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)

        super(Product, self).save()


class Image(models.Model):
    img = models.ImageField(upload_to='img/product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    def show_image(self):
        return format_html(f'<img src="{self.img.url}" width="100px" height="52.25px">')



class comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=1, blank=1,
                               verbose_name='در جواب')
    body = models.TextField(max_length=1000, verbose_name='متن')
    answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return self.body[:50]
