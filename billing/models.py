from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from account.models import Guest

User = settings.AUTH_USER_MODEL
# Create your models here.


class BillingManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            """ It's  Login User Checkout """
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            """ Guest User Checkout """
            get_email_obj = Guest.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=get_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = BillingManager()

    def __str__(self):
        return self.email

#
# def billing_profile_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.customar_id = newID
#         instance.save()
# post_save.connect(billing_profile_receiver, sender=)


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(post_save_user_receiver, sender=User)