from django.contrib.auth import get_user_model
from rest_framework import serializers

import keys
from master.serializers import VendorDataSerializer
from .models import OrderData, OrderDetailsData, InvoiceDetailsData, InvoiceData

User = get_user_model()


class OrderDataSerializer(serializers.ModelSerializer):
    purchase_order_table_id = serializers.CharField(source="id")
    vendor = serializers.SerializerMethodField()
    order_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = OrderData
        fields = [
            'id',
            'purchase_order_table_id',
            "order_id",
            "order_date",
            "vendor",
            "order_total",
            "comment",
            "transaction_type"
        ]

    def get_vendor(self, obj):
        if obj.vendor:
            return None
        return VendorDataSerializer(obj.vendor).data


class OrderDetailsDataSerializer(serializers.ModelSerializer):
    purchase_order_item_table_id = serializers.CharField(source="id")
    drug_name = serializers.CharField(source="drug.drug_name")
    purchase_order_table_id = serializers.CharField(source="purchase_order.id")

    class Meta:
        model = OrderDetailsData
        fields = [
            'id',
            'purchase_order_table_id',
            'purchase_order_item_table_id',
            "quantity",
            "expiry_date",
            "unit_price",
        ]


class InvoiceDataSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    invoice_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = InvoiceData
        fields = [
            'id',
            'invoice_id',
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
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceDetailsData
        fields = [
            'id',
            "drug_name",
            "invoice_id",
            "quantity",
            "expiry_date",
            "mrp",
            "selling_price",
            "subtotal"
        ]

    def get_subtotal(self, obj):
        return obj.subtotal()
