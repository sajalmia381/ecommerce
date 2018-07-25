from django.contrib import admin
from .models import Address
# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'address_type']
    list_filter = ['address_type']

    class Meta:
        model = Address


admin.site.register(Address, AddressAdmin)