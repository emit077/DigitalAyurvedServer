from rest_framework import serializers

from .models import MasterVendorData


class VendorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterVendorData
        fields = ["id", "vendor_name", "contact_number", "address", "reference"]
