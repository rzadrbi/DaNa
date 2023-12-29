from django.shortcuts import render
from product.models import Product, Category
from django.views.generic import DetailView, TemplateView, ListView
import requests


class ProductDetail(DetailView):
    template_name = "Product_Details.html"
    model = Product


class navbar(TemplateView):
    template_name = 'includes/NavBar_refrences.html'
    def get_context_data(self, **kwargs):
        context = super(navbar, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class product_list(ListView):
    template_name = 'product_list.html'
    queryset = Product.objects.all()
    def get_context_data(self, **kwargs):
        request = self.request
        categoty = request.GET.get('categoty')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all()
        if categoty:
            queryset = queryset.filter(categoty__title__in=categoty)
        if min_price and max_price:
            queryset = queryset.filter(price__gte= min_price, price__lte= max_price)
            queryset = queryset.order_by('price')
        context = super(product_list, self).get_context_data(**kwargs)
        context["object_list"] = queryset
        return context
