# Generated by Django 4.0.5 on 2022-07-02 18:34

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0002_rename_anupana_drugdata_anupana'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugdata',
            name='mrp',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=11),
        ),
    ]