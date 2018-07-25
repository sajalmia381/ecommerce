from django.db import models
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import order_id_generator
from billing.models import BillingProfile
from cart.models import Cart
from address.models import Address

import math
# Create your models here.

ORDER_STATUS_CHOICE = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refund', 'Refund')
)


class OrderManager(models.Manager):

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):

    billing_profile = models.ForeignKey(BillingProfile, blank=True, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=40, unique=True, blank=True)
    billing_address = models.ForeignKey(Address,
                                        related_name='billing_address',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    shipping_address = models.ForeignKey(Address,
                                         related_name='shipping_address',
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICE, default='created')
    shipping_total = models.DecimalField(max_digits=100, decimal_places=2, default=9.9)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')  # this format is  2 digits number value after info/.
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.total

        if billing_profile and billing_address and shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
            return self.status


def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = order_id_generator(instance)

    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):

    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    # instance.update_total()
    print("running")
    if created:
        print("Updating")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
