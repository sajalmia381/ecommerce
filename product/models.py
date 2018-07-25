import random
import os

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.urls import reverse

# for search
from django.db.models import Q

from product.utils import unique_slug_generator
# Create your models here.


def get_filename_ext(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


def image_path_name(instance, file_name):
    new_filename = random.randint(1, 6518489)
    name, ext = get_filename_ext(file_name)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'product/{final_filename}'.format(final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def feature(self):
        return self.filter(feature=True, active=True)

    def search(self, query):
        lookup = (
                Q(name__icontains=query) |
                Q(details__icontains=query) |
                Q(posted_on__icontains=query) |
                Q(tags__name__icontains=query)
        )
        return self.filter(lookup)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        sq = self.get_queryset().filter(id=id)  # product.objects[built_in] == get_query[default]
        if sq.count() == 1:
            return sq.first()
        return None

    def feature(self):
        return self.get_queryset().feature()

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    details = models.TextField()
    image = models.ImageField(upload_to=image_path_name)
    feature = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('product:details', kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = ['-posted_on']


def slug_save(sender, instance, *args, **kwargs):
    """
    Slug saving
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_save, sender=Product)

