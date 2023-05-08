# Register your models here.
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import BlogData


@admin.register(BlogData)
class BlogDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_data', 'created', 'modified')
    list_filter = ('created', 'modified')
