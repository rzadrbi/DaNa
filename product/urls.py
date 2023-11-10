from django.urls import path
from . import views

app_name = 'Product'

urlpatterns = [
    path('product-details/<slug:slug>', views.ProductDetail.as_view(), name='detail')
]