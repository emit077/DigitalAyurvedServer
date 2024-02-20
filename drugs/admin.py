from django.contrib import admin

from .models import DrugData


@admin.register(DrugData)
class DrugDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'drug_name',
        'formula',
        'formulation_type',
        'created',
        'modified',
    )
    search_fields = (
        'drug_name',
        'formula',
        'formulation_type',
    )
    autocomplete_fields = ['brand', 'formulation_type']
