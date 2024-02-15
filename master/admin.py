# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import MasterDoseData, MasterInstructionData, MasterFrequencyData, MasterBrandData, MasterPackagingData, \
    MasterReferenceData, MasterVendorData


@admin.register(MasterDoseData)
class MasterDoseDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'dose',
    )


@admin.register(MasterInstructionData)
class MasterInstructionDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'instruction',
    )


@admin.register(MasterFrequencyData)
class MasterFrequencyDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'frequency',
    )


@admin.register(MasterBrandData)
class MasterBrandDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand_name',
    )


@admin.register(MasterPackagingData)
class MasterPackagingDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'packaging_type',
    )


@admin.register(MasterReferenceData)
class MasterReferenceDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reference',
    )


@admin.register(MasterVendorData)
class MasterVendorDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vendor_name',
        'contact_number',
    )
    search_fields = (
        'id',
        'vendor_name',
        'contact_number',
    )
