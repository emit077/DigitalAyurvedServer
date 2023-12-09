# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import MaterDoseData, MaterInstructionData, MaterFrequencyData, MaterBrandData, MaterPackagingData, \
    MaterReferenceData, MaterVendorData


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


@admin.register(MaterBrandData)
class MaterBrandDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand_name',
    )


@admin.register(MaterPackagingData)
class MaterPackagingDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'packaging_type',
    )


@admin.register(MaterReferenceData)
class MaterReferenceDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reference',
    )


@admin.register(MaterVendorData)
class MaterVendorDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reference',
    )
