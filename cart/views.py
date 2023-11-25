from django.views.decorators.http import require_POST
from dj_shop_cart.cart import get_cart_class
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View
from product.models import Product



class CartView(View):
    def get(self, request):
        return render(request, 'cart.html', context={})


Cart = get_cart_class()


@require_POST
def add_product(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product.objects.all(), pk=product_id)
    quantity = int(request.POST.get("quantity"))
    cart = Cart.new(request)
    cart.add(product, quantity=quantity)
    ...


@require_POST
def remove_product(request: HttpRequest):
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity"))
    cart = Cart.new(request)
    cart.remove(item_id=item_id, quantity=quantity)
    ...


@require_POST
def empty_cart(request: HttpRequest):
    Cart.new(request).empty()
    ...
