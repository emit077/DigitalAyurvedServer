# Generated by Django 3.2.7 on 2024-02-01 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20240202_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicedata',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
