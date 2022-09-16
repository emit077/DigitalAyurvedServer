# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import MaterDoseData, MaterInstructionData, MaterFrequencyData


@admin.register(MaterDoseData)
class MaterDoseDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dose',
    )


@admin.register(MaterInstructionData)
class MaterInstructionDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'instruction',
    )


@admin.register(MaterFrequencyData)
class MaterFrequencyDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'frequency',
    )
