from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from dj_shop_cart.cart import get_cart_class
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views import View

from cart.models import Order, OrderItem, DiscountCode
from product.models import Product
from cart.cart import Cart


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart.html', context={'cart': cart})


class CartAddView(View):
    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        size, color, quantity = request.POST.get('size', 'سایز بندی ندار'), request.POST.get('color',
                                                                                             'رنگ بندی ندارد'), request.POST.get(
            'quantity', 'empty')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_detail')


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'order_detail.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=int(cart.total()))
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], size=item['size'], color=item['color'],
                                     quantity=item['quantity'], price=item['price'], total=item['total'])
        cart.remove_cart()
        return redirect('cart:order_detail', order.id)


class ApplyDiscountView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        code = request.POST.get('code')
        order = get_object_or_404(Order, id=order_id)
        discount_code = get_object_or_404(DiscountCode, name=code)
        OldPrice = order.total_price
        if discount_code.quantity == 0:
            return redirect('cart:order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount / 100
        NewPrice = order.total_price
        order.discount_off = OldPrice - NewPrice
        order.use_discount = True
        order.old_price = OldPrice
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order_detail', order.id)
