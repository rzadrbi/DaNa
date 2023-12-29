from django.contrib import admin
from .models import Order, OrderItem, DiscountCode


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    classes = ['collapse']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'created', 'is_paid', 'is_processed', 'is_shipped', 'use_discount']
    list_filter = ['created', 'is_paid', 'is_processed', 'is_shipped', 'use_discount']
    search_fields = ['user']
    raw_id_fields = ['user']
    inlines = [OrderItemInline]


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'quantity']
    list_filter = ['name']
    search_fields = ['name']
