from django.views.decorators.http import require_POST
from dj_shop_cart.cart import get_cart_class
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views import View
from product.models import Product


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html', context={})


Cart = get_cart_class()


class add_to_cart(View):
    def post(self, request: HttpRequest, pk):
        product = get_object_or_404(Product, id=pk)
        quantity = int(request.POST.get("quantity"))
        color = request.POST.get("color")
        size = request.POST.get("size")
        cart = Cart.new(request)
        cart.add(product, quantity=quantity)
        print('kos')
        print(cart)
        return redirect('cart:cart_detail')


# @require_POST
# def add_product(request, product_id: int):
#     product = get_object_or_404(Product.objects.all(), id=product_id)
#     quantity = int(request.POST.get("quantity"))
#     color = request.POST.get("color")
#     size = request.POST.get("size")
#     cart = Cart.new(request)
#     cart.add(product, quantity=quantity, size=size, color= color)
#     return redirect('cart:cart_detail')


@require_POST
def remove_product(request: HttpRequest):
    item_id = request.POST.get("item_id")
    quantity = int(request.POST.get("quantity"))
    cart = Cart.new(request)
    cart.remove(item_id=item_id, quantity=quantity)


@require_POST
def empty_cart(request: HttpRequest):
    Cart.new(request).empty()
