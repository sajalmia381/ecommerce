from django.urls import path

from .views import *

app_name = 'pages'

urlpatterns = [
        path('', IndexView.as_view(), name='index'),
        path('contact/', ContactView.as_view(), name='contact'),
    ]