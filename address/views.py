
from django.shortcuts import render, redirect
from .models import Address
from .forms import AddressForm
from django.utils.http import is_safe_url
from billing.models import BillingProfile
# Create your views here.


def address_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.POST.get('next')
    next_post = request.GET.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, create_billing_profile = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id

            print(instance.address_type)
            print('successful form save')
        else:
            print('error billing profile not found')
            return redirect('cart:checkout')
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('cart:checkout')
    else:
        print("form not valid")
    return redirect('cart:checkout')


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.POST.get('next')
        next_post = request.GET.get('next')
        redirect_path = next_ or next_post or None

        if request.method == "POST":
            print(request.POST)
            shipping_address = request.POST.get('shipping_address', None)
            # billing_address = request.POST.get('billing')
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, billing_profile_create = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('cart:checkout')
    return redirect('cart:checkout')
