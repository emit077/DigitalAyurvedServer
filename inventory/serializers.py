from django.contrib.auth import get_user_model
from rest_framework import serializers

import keys
from .models import OrderData, OrderDetailsData, InvoiceDetailsData, InvoiceData

User = get_user_model()


class OrderDataSerializer(serializers.ModelSerializer):
    purchase_order_table_id = serializers.CharField(source="id")
    vendor_table_id = serializers.CharField(source="vendor.id")
    vendor_name = serializers.CharField(source="vendor.vendor_name")
    order_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = OrderData
        fields = [
            'id',
            'purchase_order_table_id',
            "order_id",
            "order_date",
            "vendor_table_id",
            "vendor_name",
            "order_total",
            "comment",
            "transaction_type"
        ]



class OrderDetailsDataSerializer(serializers.ModelSerializer):
    order_items_table_id = serializers.CharField(source="id")
    drug_table_id = serializers.CharField(source="drug.id")
    drug_name = serializers.CharField(source="drug.drug_name")
    purchase_order_table_id = serializers.CharField(source="purchase_order.id")

    class Meta:
        model = OrderDetailsData
        fields = [
            'id',
            'order_items_table_id',
            'purchase_order_item_table_id',
            "drug_table_id",
            "drug_name",
            "quantity",
            "expiry_date",
            "unit_price",
        ]


class OrderDetailsAutocompleteSerializer(serializers.ModelSerializer):
    order_items_table_id = serializers.CharField(source="id")
    drug_table_id = serializers.CharField(source="drug.id")
    drug_name = serializers.CharField(source="drug.drug_name")
    brand_name = serializers.CharField(source="drug.brand.brand_name")
    expiry_date = serializers.DateField(format=keys.DATE_FORMAT)

    class Meta:
        model = OrderDetailsData
        fields = [
            'order_items_table_id',
            "drug_table_id",
            "drug_name",
            "brand_name",
            "mrp",
            "expiry_date",
            "available_qty",
        ]


class InvoiceDataSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    patient_table_id = serializers.CharField(source="patient.id")
    invoice_table_id = serializers.CharField(source="id")
    invoice_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = InvoiceData
        fields = [
            'id',
            'invoice_table_id',
            'invoice_id',
            'patient_table_id',
            'patient_name',
            'invoice_date',
            'item_total',
            'invoice_total',
            'round_off',
            'discount_amount',
            'discount_value',
            'discount_type',
            'comment',
        ]

    def get_patient_name(self, obj):
        return obj.patient.patient_name()


class InvoiceDetailsDataSerializer(serializers.ModelSerializer):
    invoice_id = serializers.CharField(source="invoice_data.invoice_id")
    drug_name = serializers.CharField(source="drug.drug_name")
    drug_table_id = serializers.CharField(source="drug.id")
    order_items_table_id = serializers.CharField(source="order_items.id")
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceDetailsData
        fields = [
            'id',
            'order_items_table_id',
            "drug_name",
            "drug_table_id",
            "invoice_id",
            "quantity",
            "expiry_date",
            "mrp",
            "selling_price",
            "subtotal"
        ]

    def get_subtotal(self, obj):
        return obj.subtotal()
