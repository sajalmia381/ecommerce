from django.db import models
from billing.models import BillingProfile

# Create your models here.

ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPE)
    address_1 = models.CharField(max_length=120)
    address_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40, default='Bangladesh')
    state = models.CharField(max_length=40)
    post_code = models.IntegerField()

    def __str__(self):
        return str(self.billing_profile)

    def get_short_address(self):
        return self.address_1

    def get_address(self):
        return "{line_1},\n{line_2},\n{city},\n{state}\n{post_code},\n{country}".format(
            line_1=self.address_1,
            line_2=self.address_2,
            city=self.city,
            state=self.state,
            post_code=self.post_code,
            country=self.country
        )
