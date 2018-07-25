from django.db import models
from product.models import Product

from django.db.models.signals import pre_save

from product.utils import unique_slug_generator
# Create your models here.


class Tags(models.Model):

    name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name


def tags_slug_save(sender, instance, *args, **kwargs):
    """
    Slug saving
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tags_slug_save, sender=Tags)