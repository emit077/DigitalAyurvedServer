# Generated by Django 3.2.7 on 2023-12-13 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0010_auto_20231213_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitemdata',
            name='expiry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
