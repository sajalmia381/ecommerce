from django.contrib import admin

from .models import Order
# Register your models here.


class OderAdmin(admin.ModelAdmin):

    list_display = ['pk', '__str__', 'cart', 'total']

    class Meta:
        model = Order


admin.site.register(Order, OderAdmin)