from django.contrib.auth import get_user_model
from django.db import models

from master.models import MasterBrandData, MasterFormulationData

Users = get_user_model()


class DrugData(models.Model):
    drug_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(to=MasterBrandData, on_delete=models.CASCADE, related_name='drug_brand')
    formulation_type = models.ForeignKey(to=MasterFormulationData, on_delete=models.CASCADE, related_name='drug_formulation',
                                    null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s|%s(%s)" % (self.id, self.drug_name, self.brand.brand_name)
