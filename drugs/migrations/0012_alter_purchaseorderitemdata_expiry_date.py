# Generated by Django 3.2.7 on 2023-12-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0011_alter_purchaseorderitemdata_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderitemdata',
            name='expiry_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
