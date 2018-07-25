from django.contrib import admin

from product.models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'posted_on', 'slug']
    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)