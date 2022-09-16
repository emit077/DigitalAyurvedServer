from django.db import models


# Create your models here.

class MaterDoseData(models.Model):
    dose = models.CharField(max_length=255, null=True)


class MaterFrequencyData(models.Model):
    frequency = models.CharField(max_length=255, null=True)


class MaterInstructionData(models.Model):
    instruction = models.CharField(max_length=255, null=True)
