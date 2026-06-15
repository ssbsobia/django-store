from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, PasswordResetToken


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_customer',
        'is_active',
    )
    list_filter = (
        'is_staff',
        'is_customer',
        'is_active',
        'is_superuser',
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Customer Info', {'fields': ('phone_no', 'is_customer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Customer Info', {'fields': ('phone_no', 'is_customer')}),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'user__username', 'token')
    readonly_fields = ('token', 'created_at')
    ordering = ('-created_at',)

