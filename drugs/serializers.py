from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DrugData

User = get_user_model()


class DrugDataSerializer(serializers.ModelSerializer):
    drug_table_id = serializers.CharField(source="id")
    brand = serializers.CharField(source="brand.brand_name")

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
        ]
