# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import PatientsData, TreatmentRecord, PrescriptionRecord


@admin.register(PatientsData)
class PatientsDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'patient_id',
        'patient_first_name',
        'patient_last_name',
        'gender',
        'age',
        'city',
        'created',
        'modified',
    )
    search_fields = (
        'patient_id',
        'user__mobile',
        'user__email',
        'patient_first_name',
        'patient_last_name',
    )




@admin.register(TreatmentRecord)
class TreatmentRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        "patient",
        "doctor",
        "chief_complaint",
        "history_of_chief_complaint",
        "blood_pressure",
        "blood_sugar",
        "plus_rate",
        "spo2",
        "temperature",
        "oe",
        'created',
        'modified',
    )
    search_fields = (
        'patient_id',
        'doctor__user__mobile',
        'doctor__user__email',
        'patient_first_name',
        'patient_last_name',
    )


@admin.register(PrescriptionRecord)
class PrescriptionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'treatment_record',
        'drug',
        'dose',
        'frequency',
        'qty',
        'instruction',
        'created',
        'modified',
    )
    search_fields = (
        'treatment_record__id',
    )
