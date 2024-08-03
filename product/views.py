from django.shortcuts import render
from product.models import Product, Category
from django.views.generic import DetailView, TemplateView, ListView
import requests


class ProductDetail(DetailView):
    template_name = "Product_Details.html"
    model = Product

    def get(self, request, *args, **kwargs):
        # override the get method
        response = super().get(request, *args, **kwargs)  # call the original get method
        self.object.view += 1  # increment the view count of the object
        self.object.save()  # save the object
        return response  # return the response


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
        cate = request.GET.getlist('cate')
        search = request.GET.get('search')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all()
        if search is not None:
            queryset = queryset.objects.filter(title__icontains=search)
        if cate:
            queryset = queryset.filter(cate__title__in=cate).distinct()
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        context = super(product_list, self).get_context_data(**kwargs)
        context["object_list"] = queryset
        context["categories"] = Category.objects.all()
        return context




