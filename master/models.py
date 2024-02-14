from django.db import models


class MasterDoseData(models.Model):
    dose = models.CharField(max_length=255, null=True)



class MasterFrequencyData(models.Model):
    frequency = models.CharField(max_length=255, null=True)



class MasterInstructionData(models.Model):
    instruction = models.CharField(max_length=255, null=True)



class MasterBrandData(models.Model):
    brand_name = models.CharField(max_length=255, null=True)



class MasterPackagingData(models.Model):
    packaging_type = models.CharField(max_length=255, null=True)



class MasterReferenceData(models.Model):
    reference = models.CharField(max_length=255, null=True)



class MasterVendorData(models.Model):
    vendor_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    reference = models.TextField(blank=True, max_length=150, null=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s|%s" % (self.vendor_name, self.contact_number)
