from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

import choices
from master.models import MaterVendorData

Users = get_user_model()


class DrugData(models.Model):
    drug_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    drug_unit = models.CharField(max_length=255, choices=choices.DRUG_UNIT, null=True, blank=True)
    anupaan = models.CharField(max_length=150, null=True, blank=True)
    formulation = models.CharField(max_length=150, null=True, blank=True)
    mrp = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PurchaseOrderData(models.Model):
    order_id = models.CharField(max_length=255)
    order_date = models.DateTimeField(null=True, blank=True)
    vendor = models.ForeignKey(to=MaterVendorData, on_delete=models.CASCADE, related_name='purchase_vendor')
    order_total = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PurchaseOrderItemData(models.Model):
    drug = models.ForeignKey(to=DrugData, on_delete=models.CASCADE, related_name='purchase_drug')
    purchase_order = models.ForeignKey(to=PurchaseOrderData, on_delete=models.CASCADE, related_name='purchase_order')
    quantity = models.CharField(max_length=255)
    expiry_date = models.DateTimeField(null=True, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
