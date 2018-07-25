from django.urls import path

from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('api/', views.cart_details_api_view, name='cart-api'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success', views.checkout_success, name='checkout-success')
]