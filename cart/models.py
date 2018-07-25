from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed
from product.models import Product

User = settings.AUTH_USER_MODEL
# Create your models here.


class CartManager(models.Manager):

    def new_or_get(self, request):

        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            print('cart ID exists')
            cart_created = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new_cart(user=None)
            cart_created = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, cart_created

    def new_cart(self, user=None, product=None):
        user_obj = None
        if user is not None:
            user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Products = models.ManyToManyField(Product, blank=True)
    sub_total = models.DecimalField(max_digits=100, decimal_places=2, blank=True, default=0)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    time_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_on = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.Products.all()
        total = 0
        for value in products:
            total += value.price
        if instance.total != total:
            instance.sub_total = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.Products.through)


def pre_save_total_receiver(sender, instance, *args, **kwargs):
    if instance.sub_total > 0:
        instance.total = instance.sub_total + 10
    else:
        instance.total = 0.00


pre_save.connect(pre_save_total_receiver, sender=Cart)
