from django.db import models


class MaterDoseData(models.Model):
    dose = models.CharField(max_length=255, null=True)



class MaterFrequencyData(models.Model):
    frequency = models.CharField(max_length=255, null=True)



class MaterInstructionData(models.Model):
    instruction = models.CharField(max_length=255, null=True)



class MaterBrandData(models.Model):
    brand_name = models.CharField(max_length=255, null=True)



class MaterPackagingData(models.Model):
    packaging_type = models.CharField(max_length=255, null=True)



class MaterReferenceData(models.Model):
    reference = models.CharField(max_length=255, null=True)



class MaterVendorData(models.Model):
    vendor_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    reference = models.TextField(blank=True, max_length=150, null=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
