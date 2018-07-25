from django.shortcuts import render, Http404, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View

from product.models import Product
from cart.models import Cart
from analytic.mixins import ObjectsViewedMixin  # Custom Signal Mixin
# Create your views here.


class ProductView(ListView):

    paginate_by = 8
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    # # Custom Model Manager Function
    # def get_object(self, *args, **kwargs):
    #     # request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("product Not Found")
    #     return instance

    # # class Base Models Manager Buildin Function
    # def get_queryset(self, *args, **kargs):
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)


class ProductDetails(ObjectsViewedMixin, DetailView):

    template_name = 'product/product_detail.html'
    # model = Product

    #  Custom models manger queryset
    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     print(request)
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404('Item Not Found')
    #     return instance

    # class Base view BuildIn function
    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request)
        pk = self.kwargs.get('pk')
        instance = Product.objects.filter(pk=pk)
        return instance


class ProductSlugDetails(ObjectsViewedMixin, DetailView):

    queryset = Product.objects.all()
    template_name = 'product/product_detail.html'
    context_object_name = 'object'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetails, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    # def get_queryset(self, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     return Product.objects.filter(slug=slug)

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug, active=True)
        # try:
        #     instance = Product.objects.filter(slug=slug, active=True)
        # except Product.DoesNotExist:
        #     raise Http404('Product Not Found')
        # except Product.MultipleObjectsReturned:
        #     qs = Product.objects.filter(slug=slug, active=True)
        #     instance = qs.first()
        # except:
        #     raise Http404('Uff Product HTTP 404 Error')

        # object_viewed_signal.send(instance.__class__, instance=instance, request=request) # for it make custom mixin is ObjectsViewedMixin

        return instance


class ProductFeature(ListView):
    queryset = Product.objects.feature()  # [Custom Queryset]
    template_name = 'product/product_list.html'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(ProductFeature, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    #
    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductFeature, self).get_context_data(*args, **kwargs)
    #     # print(context)
    #     return context

    # # Custom Model Manager Function
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     print(request)
    #     return Product.objects.feature()


class ProductFeatureDetails(ObjectsViewedMixin, DetailView):

    template_name = 'product/product_detail.html'
    queryset = Product.objects.feature()

