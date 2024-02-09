# Register your models here.
from django.contrib import admin

from .models import OrderData, OrderDetailsData, InvoiceDetailsData, InvoiceData


@admin.register(OrderData)
class OrderDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_id',
        'vendor',
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


@admin.register(InvoiceData)
class InvoiceDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice_id',
        'patient',
        'invoice_date',
        "item_total",
        "invoice_total",
        "round_off",
        "discount_amount",
        "discount_value",
        "discount_type",

        'created',
        'modified',
    )
    search_fields = (
        'invoice_id',
        'invoice_date',
    )
    autocomplete_fields = ['patient']
    readonly_fields = ('invoice_id',)


@admin.register(InvoiceDetailsData)
class InvoiceDetailsDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'drug',
        'invoice_data',
        'quantity',
        'expiry_date',
        'mrp',
        'selling_price',
        'created',
        'modified',
    )
    search_fields = ()
    autocomplete_fields = ['drug']
