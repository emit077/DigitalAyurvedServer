# Generated by Django 3.2.7 on 2023-12-13 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0014_alter_purchaseorderdata_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderdata',
            name='order_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]