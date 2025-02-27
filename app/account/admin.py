from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'full_name']
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'first_name',
            'last_name',
            'is_writer'
        )}),
        (
            _('Permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('date_joined', 'last_login',)}),
    )
    readonly_fields = ['date_joined', 'last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
