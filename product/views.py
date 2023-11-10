from django.shortcuts import render
from django.views.generic import DetailView

from product.models import Product


class ProductDetail(DetailView):
    template_name = "Product_Details.html"
    model = Product

