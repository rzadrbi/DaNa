from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('datail', views.CartView.as_view(), name='cart_detail'),
    path('add/<int:id>', views.CartAddView.as_view(), name='cart_add'),
    path('remove/<str:id>', views.CartDeleteView.as_view(), name='cart_remove'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/add', views.OrderCreateView.as_view(), name='order_create'),
    path('apply/discount/<int:order_id>/', views.ApplyDiscountView.as_view(), name='apply_discount'),
    # path('empty', views.empty_cart, name='cart_empty'),
]
