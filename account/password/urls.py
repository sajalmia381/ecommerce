from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('password/change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_view.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('password/reset/\(?P<uidb64>[0-9A-Za-z_\-]+)/\(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #      auth_view.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    path('password/reset/complete/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]