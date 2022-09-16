from django.contrib import admin

# Register your models here.
from .models import DoctorsData


# Register your models here.

@admin.register(DoctorsData)
class DoctorsDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dob', "degree", "medical_reg_no", "city", "created", "modified"]
    search_fields = ['user__mobile', "user__name", 'user__email', ]
    autocomplete_fields = ['user']
    # list_filter = ['is_active', "account_type"]
