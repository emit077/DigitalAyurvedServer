from django.contrib.auth import get_user_model
from rest_framework import serializers

import keys
from .models import DrugData, PurchaseOrderData, PurchaseOrderItemData

User = get_user_model()


class DrugDataSerializer(serializers.ModelSerializer):
    drug_table_id = serializers.CharField(source="id")

    class Meta:
        model = DrugData
        fields = [
            'id',
            'drug_table_id',
            "drug_name",
            "formula",
            "brand",
            "mrp",
            "drug_unit",
            "anupaan",
            "formulation",
        ]


class PurchaseOrderDataSerializer(serializers.ModelSerializer):
    purchase_order_table_id = serializers.CharField(source="id")
    vendor_table_id = serializers.CharField(source="vendor.id")
    vendor_name = serializers.CharField(source="vendor.vendor_name")
    order_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = PurchaseOrderData
        fields = [
            'id',
            'purchase_order_table_id',
            "order_id",
            "order_date",
            "vendor_name",
            "vendor_table_id",
            "order_total",
        ]


class PurchaseOrderItemDataSerializer(serializers.ModelSerializer):
    purchase_order_item_table_id = serializers.CharField(source="id")
    drug_name = serializers.CharField(source="drug.drug_name")
    purchase_order_table_id = serializers.CharField(source="purchase_order.id")

    class Meta:
        model = PurchaseOrderItemData
        fields = [
            'id',
            'purchase_order_table_id',
            'purchase_order_item_table_id',
            "quantity",
            "expiry_date",
            "unit_price",
        ]
