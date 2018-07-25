from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from .utils import MailChimp
# Create your models here.


class MarketingPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=True)
    mailchimp_mes = models.TextField(null=True, blank=True)
    timestremp = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


def marking_pre_update_reciver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = MailChimp().subscribe(instance.user.email)
        print(status_code, response_data)


post_save.connect(marking_pre_update_reciver, sender=MarketingPreference)


def make_marketing_pre_reciver(sender, instance, created, *args, **kwargs):
    if created:
        MarketingPreference.object.get_or_create(user=instance)


post_save.connect(make_marketing_pre_reciver, sender=settings.AUTH_USER_MODEL)