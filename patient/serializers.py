from django.contrib.auth import get_user_model
from rest_framework import serializers

import keys
from .models import PatientsData, PrescriptionRecord, TreatmentRecord

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


class TreatmentRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.name")
    doctor_mobile = serializers.CharField(source="doctor.user.mobile")
    patient_name = serializers.CharField(source="doctor.user.name")
    patient_mobile = serializers.CharField(source="doctor.user.mobile")
    created = serializers.DateTimeField(format=keys.DATE_TIME_FORMAT)

    class Meta:
        model = TreatmentRecord
        fields = ['id',
                  'doctor_name',
                  'doctor_mobile',
                  'patient_name',
                  'patient_mobile',
                  'chief_complaint',
                  'history_of_chief_complaint',
                  'required_test',
                  'advise',
                  'created'
                  ]
