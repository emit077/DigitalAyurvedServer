from django.db import models


# Create your models here.

class EnquiryData(models.Model):
    name = models.CharField(max_length=255, null=True)
    mobile = models.CharField(unique=True, max_length=10)
    email = models.EmailField(blank=True, verbose_name='email', null=True)
    message = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s | %s " % (self.id, self.name, self.mobile)
