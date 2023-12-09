from rest_framework import serializers

import keys
from .models import EnquiryData


class EnquiryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryData
        fields = ['id', keys.NAME, keys.MOBILE, keys.EMAIL, keys.MESSAGE]
