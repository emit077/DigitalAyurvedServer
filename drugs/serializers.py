from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DrugData

User = get_user_model()


class DrugDataSerializer(serializers.ModelSerializer):
    drug_table_id = serializers.CharField(source="id")
    brand = serializers.CharField(source="brand.brand_name")
    available_qty = serializers.SerializerMethodField()

    class Meta:
        model = DrugData
        fields = [
            'id',
            'drug_table_id',
            "drug_name",
            "brand",
            "formula",
            "mrp",
            "drug_unit",
            "anupaan",
            "formulation",
            "available_qty",
        ]

    def get_available_qty(self, obj):
        return obj.available_qty if obj.available_qty else "0"


class BestSellerDrugSerializer(serializers.ModelSerializer):
    drug_table_id = serializers.CharField(source="id")
    brand = serializers.CharField(source="brand.brand_name")
    quantity = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = DrugData
        fields = [
            'id',
            'drug_table_id',
            "drug_name",
            "brand",
            "quantity",
            "amount"
        ]

    def get_quantity(self, obj):
        return obj.quantity if obj.quantity else "0"
    def get_amount(self, obj):
        return obj.amount if obj.amount else "0"
