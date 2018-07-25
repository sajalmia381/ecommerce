from django.shortcuts import render, redirect
from order.models import Order
from product.models import Product
from billing.models import BillingProfile
from account.forms import GuestForm
from account.models import Guest
from address.forms import AddressForm
from address.models import Address
from django.http import JsonResponse

from cart.models import Cart
# Create your views here.


def cart_details_api_view(request):
    """ cart home update Ajax view """
    cart_obj, cart_obj_create = Cart.objects.new_or_get(request)

    products = [{
        'id': x.id,
        'name': x.name,
        'price': x.price,
        'url': x.get_absolute_url(),
    } for x in cart_obj.Products.all()]
    # Note this is just like up products = [{'name': x.name, 'price': x.price, } for x in cart_obj.Products.all()]
    # products_list = {}
    # for x in cart_obj.Products.all():
    #     products_list.append(
    #         {'name': x .name, 'price': x.price}
    #     )

    cart_data = {'products': products, 'sub_total': cart_obj.sub_total, 'total': cart_obj.total}
    return JsonResponse(cart_data)

# def cart_create(user=None):
#
#     cart_obj = Cart.objects.create(user=None)
#     print("new cart Created")
#     return cart_obj


def cart_view(request):

    """
    * ===================================     goes in models manager

    cart_id = request.session.get('cart_id', None)
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        print('cart ID exists')
        cart_obj = qs.first()
        if request.user.is_authenticated and cart_obj.user is None:
            cart_obj.user = request.user
            cart_obj.save()
    else:
        cart_obj = Cart.objects.new_cart(user=None)
        request.session['cart_id'] = cart_obj.id
    """
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.Products.all()
    total = 0
    for value in products:
        total += value.price
    print(total)
    cart_obj.total = total
    cart_obj.save()
    return render(request, 'cart/cart.html', {'products': products, 'cart': cart_obj})


def cart_update(request):
    # print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # print("product Not Exists")
            return redirect('cart:cart')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.Products.all():
            cart_obj.Products.remove(product_obj)
            added = False
        else:
            cart_obj.Products.add(product_obj)
            added = True

        request.session['cart_item'] = cart_obj.Products.count()

        if request.is_ajax():
            print("a Ajax Request")
            # print("ajax request is: ", request.is_ajax())
            data = {
                "added": added,
                "removed": not added,
                'cartItemCount': cart_obj.Products.count()
            }
            return JsonResponse(data, status=200)
    return redirect('cart:cart')


def checkout_view(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.Products.count() == 0:
        return redirect('cart:cart')
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, created_billing_profile = BillingProfile.objects.new_or_get(request)
    qs_address = None
    if billing_profile is not None:

        if request.user.is_authenticated:
            qs_address = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == 'POST':
        """ Make Order Completed """
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_item'] = 0
            return redirect("cart:checkout-success")

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'guest_form': guest_form,
        'address_form': address_form,
        'qs_address': qs_address,
    }
    return render(request, 'cart/checkout.html', context)


def checkout_success(request):
    return render(request, 'cart/checkout_success.html')