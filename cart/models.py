from django.db import models

from account.models import User
from product.models import Product
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('user'))
    total_price = models.PositiveBigIntegerField(default=0, verbose_name=_('total_price'))
    address = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('address'))
    is_paid = models.BooleanField(default=False, verbose_name=_('پرداخت شده'))
    is_processed = models.BooleanField(default=False, verbose_name=_('پردازش شده'))
    is_shipped = models.BooleanField(default=False, verbose_name=_('ارسال شده'))
    use_discount = models.BooleanField(default=False, verbose_name=_('استفاده از کد تخفیف'))
    discount_off = models.IntegerField(default=0, verbose_name=_('مقدار تخفیف اعمال شده'))
    old_price = models.PositiveBigIntegerField(default=0, verbose_name=_('قیمت قبلی'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    discount = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name=_('تخفیف محصول'))

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارش ها')

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name=_('product'))
    size = models.CharField(max_length=100, verbose_name=_('size'))
    total = models.PositiveBigIntegerField(default=0, verbose_name=_('total'))
    color = models.CharField(max_length=100, verbose_name=_('color'))
    quantity = models.PositiveBigIntegerField(verbose_name=_('quantity'))
    price = models.PositiveBigIntegerField(verbose_name=_('price'))
    discount = models.PositiveSmallIntegerField(default=0, null=True, blank=True, verbose_name=_('تخفیف محصول'))
    class Meta:
        verbose_name = _('OrderItems')
        verbose_name_plural = _('OrderItems')

    def __str__(self):
        return self.order.user.phone


class DiscountCode(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('name'))
    discount = models.PositiveSmallIntegerField(default=0, verbose_name=_('discount'))
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('DiscountCode')
        verbose_name_plural = _('DiscountCodes')

    def __str__(self):
        return self.name


class shipping_cost(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('روش پستی'))
    price = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = _('روش پست')
        verbose_name_plural = _('روش های پستی')

    def __str__(self):
        return self.title
