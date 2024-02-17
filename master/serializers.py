from rest_framework import serializers

from .models import MasterVendorData, MasterBrandData, MasterFormulationData


class VendorDataSerializer(serializers.ModelSerializer):
    vendor_table_id = serializers.CharField(source="id")

    class Meta:
        model = MasterVendorData
        fields = ["id", "vendor_table_id", "vendor_name", "contact_number", "address", "reference"]


class MasterBrandDataSerializer(serializers.ModelSerializer):
    brand_table_id = serializers.CharField(source="id")

    class Meta:
        model = MasterBrandData
        fields = ["id", "brand_table_id", "brand_name"]


class MasterFormulationDataSerializer(serializers.ModelSerializer):
    formulation_table_id = serializers.CharField(source="id")

    class Meta:
        model = MasterFormulationData
        fields = ["id", "formulation_table_id", "formulation_type"]
