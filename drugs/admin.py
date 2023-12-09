from django.contrib import admin

from .models import DrugData, PurchaseOrderData, PurchaseOrderItemData


@admin.register(DrugData)
class DrugDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'drug_name',
        'formula',
        'brand',
        'drug_unit',
        'anupaan',
        'formulation',
        'mrp',
        'created',
        'modified',
    )
    search_fields = (
        'drug_name',
        'formula',
        'brand',
    )


@admin.register(PurchaseOrderData)
class PurchaseOrderDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_id',
        'order_date',
        'created',
        'modified',
    )
    search_fields = (
        'order_id',
        'order_date',
    )
@admin.register(PurchaseOrderItemData)
class PurchaseOrderItemDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'quantity',
        'expiry_date',
        'created',
        'modified',
    )
    search_fields = (
    )