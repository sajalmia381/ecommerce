from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, RegistrationView, guest_view, AccountDashBroad

app_name = 'account'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/guest', guest_view, name='registration-guest'),
    path('dashbroad/', AccountDashBroad.as_view(), name='account-dashbroad'),
]