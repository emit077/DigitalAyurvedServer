from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

import choices
from doctor.models import DoctorsData
from drugs.models import DrugData

Users = get_user_model()


class PatientsData(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE, related_name='patient_user', null=True, blank=True)
    patient_id = models.CharField(max_length=15, null=True)
    patient_first_name = models.CharField(max_length=255, null=True)
    patient_last_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=100, choices=choices.GENDER_CHOICE)
    occupation = models.CharField(max_length=255, null=True)
    age = models.PositiveIntegerField(default=1)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s | %s " % (self.patient_first_name, self.patient_last_name, self.user.mobile)

    def patient_name(self):
        return self.patient_first_name + " " + self.patient_last_name


class TreatmentRecord(models.Model):
    patient = models.ForeignKey(to=PatientsData, on_delete=models.CASCADE, related_name='patient_record', )
    doctor = models.ForeignKey(to=DoctorsData, on_delete=models.CASCADE, related_name='doctor_record', )
    chief_complaint = models.TextField()
    history_of_chief_complaint = models.TextField()
    blood_pressure = models.CharField(max_length=50, null=True, blank=True)
    blood_sugar = models.PositiveIntegerField(default=0)
    plus_rate = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    spo2 = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    weight = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    temperature = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    oe = models.TextField(null=True, blank=True, help_text="on examination")
    diet_exercise = models.TextField(null=True, blank=True, help_text="on examination")
    required_test = models.TextField(null=True, blank=True)
    advise = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class PrescriptionRecord(models.Model):
    treatment_record = models.ForeignKey(to=TreatmentRecord, on_delete=models.CASCADE, related_name='treatment_prescription',)
    drug = models.ForeignKey(to=DrugData, on_delete=models.CASCADE, related_name='prescription_drug')
    dose = models.CharField(max_length=400, null=True, blank=True)
    frequency = models.CharField(max_length=400, null=True, blank=True)
    qty = models.CharField(max_length=400, null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.treatment_record.patient.user.name)
