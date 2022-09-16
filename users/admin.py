from django.contrib import admin

# Register your models here.
from .models import CustomUser


# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'mobile', "name", 'email', 'is_active', "account_type", "created", "modified"]
    search_fields = ['id', 'mobile', "name", 'email', 'is_active', "account_type"]
    list_filter = ['is_active', "account_type"]
