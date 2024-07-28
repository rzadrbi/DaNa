from django.contrib import admin
from home.models import contact_phone


@admin.register(contact_phone)
class contact_phoneAdmin(admin.ModelAdmin):
    list_display = ('phone', )


