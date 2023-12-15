from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        contex = super(Home, self).get_context_data(**kwargs)
        return contex
