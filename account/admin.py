from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Guest
# Register your models here.

User = get_user_model()


class CustomUserAdmin(UserAdmin):

    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    search_fields = ['email', 'full_name', 'admin', 'staff', 'is_active']
    list_display = ['email', 'admin', 'staff', 'is_active']
    list_filter = ['admin', 'staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Full name', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin', 'staff',)}),
    )

    add_fieldsets = (
        (None, {
            # 'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)

admin.site.register(Guest)
