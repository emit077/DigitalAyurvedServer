from django.db import models

# Create your models here.
class BlogData(models.Model):
    blog_data = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)