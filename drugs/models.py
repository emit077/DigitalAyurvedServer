from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

import choices

Users = get_user_model()


class DrugData(models.Model):
    drug_name = models.CharField(max_length=255, null=True)
    formula = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=100, )
    drug_unit = models.CharField(max_length=255, choices=choices.DRUG_UNIT)
    anupana = models.CharField(max_length=150)
    formulation = models.CharField(max_length=150)
    mrp = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
