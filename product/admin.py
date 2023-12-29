from django.contrib import admin
from django.utils.html import format_html

from . import models


class PicInline(admin.TabularInline):
    model = models.Image
    fields = ('img', 'product',)
    readonly_fields = ('image_tag', )

    def image_tag(self, obj):
        return format_html('<img src="{}" width="150" height="150"/>', obj.image.url)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('cate', 'brand')
    search_fields = ('title', '')
    list_display = ('title', 'brand',)
    inlines = (PicInline, )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('title', 'parent',)
    list_display = ('title', 'parent',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Brand)
class ModelNameAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(models.Color)
class ModelNameAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(models.Size)
class ModelNameAdmin(admin.ModelAdmin):
    list_filter = ('title',)


@admin.register(models.Image)
class ModelNameAdmin(admin.ModelAdmin):
    list_filter = ('product',)
    list_display = ('product',)


@admin.register(models.comment)
class ModelNameAdmin(admin.ModelAdmin):
    list_filter = ('answered',)
    list_display = ('product', 'user')

