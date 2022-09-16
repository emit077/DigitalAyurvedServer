from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import PatientsData, PrescriptionRecord

User = get_user_model()


class PatientsDataSerializer(serializers.ModelSerializer):
    patient_table_id = serializers.CharField(source="id")
    user_table_id = serializers.CharField(source="user.id")
    name = serializers.CharField(source="user.name")
    mobile = serializers.CharField(source="user.mobile")
    email = serializers.CharField(source="user.email")
    is_active = serializers.BooleanField(source="user.is_active")

    class Meta:
        model = PatientsData
        fields = ['patient_table_id',
                  'user_table_id',
                  'is_active',
                  'name',
                  'mobile',
                  'email',
                  'gender',
                  'age',
                  'address',
                  'city',
                  "patient_first_name",
                  "patient_last_name",
                  "occupation",
                  ]


class PrescriptionRecordSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.drug_name")
    class Meta:
        model = PrescriptionRecord
        fields = ['id',
                  'drug',
                  'drug_name',
                  'dose',
                  'frequency',
                  'qty',
                  'instruction',
                  ]
