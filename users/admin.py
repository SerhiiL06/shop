from django.contrib import admin
from .models import User, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']
    ordering = ['username']


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    fields = ['user', 'code', 'created', 'expiration']
    readonly_fields = ['code', 'created', 'expiration']