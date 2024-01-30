# Register your models here.
from django.contrib import admin

from .models import OrderData, OrderDetailsData


@admin.register(OrderData)
class OrderDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_id',
        'vendor',
        'patient',
        'order_date',
        'created',
        'modified',
    )
    search_fields = (
        'order_id',
        'order_date',
    )
    autocomplete_fields = ['vendor']
    readonly_fields = ('order_id',)


@admin.register(OrderDetailsData)
class OrderDetailsDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'quantity',
        'expiry_date',
        'created',
        'modified',
    )
    search_fields = ()
    autocomplete_fields = ['drug']
