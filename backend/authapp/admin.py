from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class Admin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    fieldsets = ((None, {
        'fields': ('username', 'password')
    }),
    ('Info', {
        'fields': ('first_name', 'last_name', 'email')
    }),
    ('Permissions', {
        'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    }))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',)}
         ),
    )
    ordering = ('last_name', 'first_name',)

    class Meta:
        model = User


admin.site.register(User, Admin)
