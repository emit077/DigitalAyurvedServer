from django.contrib.auth import get_user_model
from django.db import models

import choices

Users = get_user_model()


class DoctorsData(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE, related_name='doctor_user')
    dob = models.DateField(max_length=70, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True)
    medical_reg_no = models.CharField(max_length=150)
    designation = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=70, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=choices.GENDER_CHOICE)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s | %s " % (self.user.name, self.user.mobile)
