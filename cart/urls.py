from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('datail', views.CartView.as_view(), name='cart_detail'),
    path('add/<int:pk>', views.add_to_cart.as_view(), name='cart_add'),
    path('remove', views.remove_product, name='cart_remove'),
    path('empty', views.empty_cart, name='cart_empty'),
]
