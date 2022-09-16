from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import DoctorsData

User = get_user_model()


class DoctorDataSerializer(serializers.ModelSerializer):
    doctor_table_id = serializers.CharField(source="id")
    user_table_id = serializers.CharField(source="user.id")
    name = serializers.CharField(source="user.name")
    mobile = serializers.CharField(source="user.mobile")
    email = serializers.CharField(source="user.email")
    is_active = serializers.BooleanField(source="user.is_active")

    class Meta:
        model = DoctorsData
        fields = ['doctor_table_id',
                  'user_table_id',
                  'is_active',
                  'name',
                  'mobile',
                  'email',
                  'gender',
                  'dob',
                  'degree',
                  'medical_reg_no',
                  'designation',
                  'address',
                  'city',
                  ]
