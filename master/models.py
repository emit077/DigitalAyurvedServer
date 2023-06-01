from django.db import models


# Create your models here.

class MaterDoseData(models.Model):
    dose = models.CharField(max_length=255, null=True)


class MaterFrequencyData(models.Model):
    frequency = models.CharField(max_length=255, null=True)


class MaterInstructionData(models.Model):
    instruction = models.CharField(max_length=255, null=True)


class MasterBrandData(models.Model):
    brand_name = models.CharField(max_length=255, null=True)


class MasterPackagingTypeData(models.Model):
    packing_type = models.CharField(max_length=255, null=True)


class MasterFormulaReferenceData(models.Model):
    reference_type = models.CharField(max_length=255, null=True)


class MasterVendorData(models.Model):
    vendor_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    reference = models.TextField(max_length=150, null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
