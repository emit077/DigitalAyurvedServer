from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DrugData

User = get_user_model()


class DrugDataSerializer(serializers.ModelSerializer):
    drug_table_id = serializers.CharField(source="id")

    class Meta:
        model = DrugData
        fields = ['drug_table_id',
                  "drug_name",
                  "formula",
                  "brand",
                  "mrp",
                  "drug_unit",
                  "anupana",
                  "formulation",
                  ]
