from django.contrib.auth import get_user_model
from django.db import models

import choices
import keys
from master.models import MasterBrandData, MasterPackagingTypeData, MasterFormulaReferenceData, MasterVendorData

Users = get_user_model()


class DrugData(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=choices.ITEM_CATEGORY, default=keys.DRUG)
    formula = models.CharField(max_length=255, null=True, blank=True)
    drug_type = models.CharField(max_length=255, null=True, blank=True, choices=choices.DRUG_TYPE,
                                 default=choices.DRUG_TYPE[0][0])
    brand = models.ForeignKey(to=MasterBrandData, null=True, blank=True, on_delete=models.CASCADE,
                              related_name='drug_brand')
    packaging_type = models.ForeignKey(to=MasterPackagingTypeData, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='packaging_type')
    formula_reference = models.ForeignKey(to=MasterFormulaReferenceData, null=True, blank=True,
                                          on_delete=models.CASCADE,
                                          related_name='drug_brand')
    drug_unit = models.CharField(max_length=255, choices=choices.DRUG_UNIT, null=True, blank=True)
    anupaan = models.CharField(max_length=150, null=True, blank=True)
    formulation = models.CharField(max_length=150, null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PurchaseOrderData(models.Model):
    vendor = models.ForeignKey(to=MasterVendorData, on_delete=models.CASCADE, related_name='drug_brand')
    invoice_id = models.CharField(max_length=150, null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(max_length=150, null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PurchaseItemData(models.Model):
    purchase_order = models.ForeignKey(to=PurchaseOrderData, on_delete=models.CASCADE, related_name='drug_brand')
    drug = models.ForeignKey(to=DrugData, on_delete=models.CASCADE, related_name='drug_brand')
    qty = models.CharField(max_length=150, null=True, blank=True)
    purchase_price = models.FloatField(default=0, help_text="unit purchase price")
    mrp = models.FloatField(default=0, help_text="unit item MRP")
    expiry_date = models.DateTimeField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
