from rest_framework import serializers

from .models import MasterVendorData


class VendorDataSerializer(serializers.ModelSerializer):
    vendor_table_id = serializers.CharField(source="id")

    class Meta:
        model = MasterVendorData
        fields = ["id", "vendor_table_id", "vendor_name", "contact_number", "address", "reference"]
