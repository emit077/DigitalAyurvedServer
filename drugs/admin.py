from django.contrib import admin

from .models import DrugData


@admin.register(DrugData)
class DrugDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'drug_name',
        'formula',
        'brand',
        'drug_unit',
        'anupana',
        'formulation',
        'mrp',
        'created',
        'modified',
    )
    search_fields = (
        'drug_name',
        'formula',
        'brand',
    )
