from django.shortcuts import render
from django.views.generic import TemplateView, ListView
# Create your views here.

from product.models import Product


class SearchView(ListView):

    template_name = 'search/search_list.html'

    def get_queryset(self, *args, **kwargs):

        print(self.request.GET)
        query = self.request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.feature()