# Generated by Django 3.2.7 on 2023-12-13 12:38

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0009_purchaseorderdata_purchaseorderitemdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderdata',
            name='order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorderdata',
            name='order_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=11, null=True),
        ),
    ]
