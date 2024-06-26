from django.shortcuts import render
from django.views.generic import TemplateView

from product.models import Product


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        offer_product = Product.objects.filter(discount__gt=44).first()
        arival_product = Product.objects.all()[:8]
        contex = super(Home, self).get_context_data(**kwargs)
        contex['offer_product'] = offer_product
        contex['arival_product'] = arival_product
        return contex


def page_not_found(request, exception):
    return render(request, '404.html')