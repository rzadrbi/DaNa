from django.views.decorators.http import require_POST
from dj_shop_cart.cart import get_cart_class
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views import View
from product.models import Product
from cart.cart import Cart


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart.html', context={'cart': cart})

class CartAddView(View):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        size, color, quantity = request.POST.get('size', 'سایز بندی ندار'), request.POST.get('color', 'رنگ بندی ندارد'), request.POST.get(
            'quantity', 'empty')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_detail')

class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')
