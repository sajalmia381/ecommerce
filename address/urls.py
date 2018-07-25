from django.urls import path
from .views import address_view, checkout_address_reuse_view

app_name = 'address'

urlpatterns = [
    path('address-form', address_view, name='address-form'),
    path('address-reuse', checkout_address_reuse_view, name='address-reuse'),
]