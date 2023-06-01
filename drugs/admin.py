
from django.contrib import admin

from .models import DrugData, PurchaseOrderData, PurchaseItemData


@admin.register(DrugData)
class DrugDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'formula',
        'drug_type',
        'brand',
        'packaging_type',
        'formula_reference',
        'drug_unit',
        'anupaan',
        'formulation',
        'created',
        'modified',
    )
    list_filter = (
        'category',
        'packaging_type',
        'formula_reference',
        'created',
        'modified',
    )
    search_fields = ('name',)


@admin.register(PurchaseOrderData)
class PurchaseOrderDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vendor',
        'invoice_id',
        'invoice_date',
        'comment',
        'created',
        'modified',
    )
    list_filter = ('invoice_date', 'created', 'modified')


@admin.register(PurchaseItemData)
class PurchaseItemDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'purchase_order',
        'drug',
        'qty',
        'purchase_price',
        'mrp',
        'expiry_date',
        'created',
        'modified',
    )
    list_filter = (
        'purchase_order',
        'drug',
        'expiry_date',
        'created',
        'modified',
    )
