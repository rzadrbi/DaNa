import requests
from django.shortcuts import render
from product.models import Product
from django.views.generic import DetailView


class ProductDetail(DetailView):
    template_name = "Product_Details.html"
    model = Product
