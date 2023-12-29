from django.urls import path
from . import views

app_name = 'Product'

urlpatterns = [
    path('product_list', views.product_list.as_view(), name='list'),
    path('product_details/<slug:slug>', views.ProductDetail.as_view(), name='detail'),
    path('navbar', views.navbar.as_view(), name='navbar'),
]