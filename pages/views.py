from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, FormView, View, CreateView
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from product.models import Product
from .forms import ContactForm
# Create your views here.


class IndexView(ListView):

    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):

        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['heading'] = 'Welcome to eCommerce site'
        return context

    def get_queryset(self):
        # self.feature = get_object_or_404(Product, feature=True)

        return Product.objects.feature()


class ContactView(CreateView):

    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:contact')


# class ContactView(FormView):
#
#     template_name = 'contact/contact.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('pages:contact')
#
#     def form_valid(self, form):
#         # subject = 'subject: contact submit confirm'
#         # from_email = settings.DEFAULT_FROM_EMAIL
#         # message = 'Message: Thanks you. We reply very soon! :)'
#         # recipient_list = [settings.EMAIL_HOST_USER, '{}'.format(form.cleaned_data.get('email'))]
#         # html_message = '<h1>html_message: Thanks you. We reply very soon! :)</h1>'
#         #
#         # send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=False)
#         # print("successful")
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         print('Form not valid')
#         return super().form_invalid(form)


    # def form_valid(self, form):
    #     request = self.request
    #     form = ContactForm(request.POST or None)
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         instance.save()
    #         if request.is_ajax:
    #             return JsonResponse({"message": "success Json Response"})
    #         return redirect('pages:contact')
    #     if form.errors:
    #         if request.is_ajax:
    #             return JsonResponse({"error": "Form Not sending error from Json"})
    #     return super().form_valid()

# class ContactView(View):
#
#     template_name = 'contact/contact.html'
#
#     def get(self, request):
#         form = ContactForm(request.POST or None)
#         print(form)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = ContactForm(request.POST or None)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             if request.is_ajax:
#                 return JsonResponse({"message": "success Json Response"})
#             return redirect('pages:contact')
#         if form.errors:
#             if request.is_ajax:
#                 return JsonResponse({"error": "Form Not sending error from Json"})
#         return render(request, self.template_name, {'form': form})