from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, FormView, DetailView, RedirectView
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from django.http import JsonResponse
from .forms import UserRegistrationForm, GuestForm, LoginForm
from .models import Guest
from .signal import user_logged_in
# Create your views here.


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.POST.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth = authenticate(request, password=password, username=username)
        if auth is not None:
            login(request, auth)
            user_logged_in.send(auth.__class__, instance=auth, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('pages:index')
            if request.is_ajax:
                return JsonResponse({'success': 'form Successfully Save'})
            return redirect('account:login')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


# class LoginView(View):
#     templates_name = 'account/login.html'
#
#     def get(self, request):
#         form = LoginForm(request.POST or None)
#         return render(request, self.templates_name, {"form": form})
#
#     def post(self, request):
#         form = LoginForm(request.POST or None)
#         next_ = request.POST.get('next')
#         next_post = request.GET.get('next')
#         redirect_path = next_ or next_post or None
#         if form.is_valid():
#             username = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             auth = authenticate(request, password=password, username=username)
#             if auth is not None:
#                 login(request, auth)
#                 try:
#                     del request.session['guest_email_id']
#                 except:
#                     pass
#                 if is_safe_url(redirect_path, request.get_host()):
#                     return redirect(redirect_path)
#                 else:
#                     return redirect('pages:index')
#             else:
#                 print('login errors')
#         return render(request, self.templates_name, {"form": form})

#
# def registration_view(request):
#     if request.user.is_authenticated:
#         return redirect('pages:index')
#     else:
#         form = UserRegistrationForm(request.POST or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#         return render(request, 'account/registration.html', {'form': form})


class RegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/registration.html'
    success_url = reverse_lazy('account:login')


def guest_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.POST.get('next')
    next_post = request.GET.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = Guest.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('cart:checkout')


# class LoginRequireView(object):
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super(AccountDashBroad, self).dispatch(self, request, *args, **kwargs)


class AccountDashBroad(LoginRequiredMixin, DetailView):
    template_name = 'account/account-dash-broad.html'

    def get_object(self, queryset=None):
        return self.request.user

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(AccountDashBroad, self).dispatch(self, request, *args, **kwargs)
