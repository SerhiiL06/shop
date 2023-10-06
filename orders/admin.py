from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'initiator']
    fields = (
        'initiator',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'created',
        'status',
        'basket_history',
    )
    readonly_fields = ['created', 'initiator']
