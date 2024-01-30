from django.contrib.auth import get_user_model
from rest_framework import serializers

import keys
from master.serializers import VendorDataSerializer
from patient.serializers import PatientsDataSerializer
from .models import OrderData, OrderDetailsData

User = get_user_model()


class InOutItemDataSerializer(serializers.ModelSerializer):
    purchase_order_table_id = serializers.CharField(source="id")
    vendor = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    order_date = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = OrderData
        fields = [
            'id',
            'purchase_order_table_id',
            "order_id",
            "order_date",
            "vendor",
            "patient",
            "order_total",
            "comment",
            "transaction_type"
        ]

    def get_vendor(self, obj):
        if obj.vendor:
            return None
        return VendorDataSerializer(obj.vendor).data

    def get_patient(self, obj):
        if obj.patient:
            return None
        return PatientsDataSerializer(obj.patient).data



class InOutItemDetailsDataSerializer(serializers.ModelSerializer):
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
