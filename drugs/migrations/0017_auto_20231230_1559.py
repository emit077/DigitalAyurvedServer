# Generated by Django 3.2.7 on 2023-12-30 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0016_alter_purchaseorderitemdata_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorderitemdata',
            name='drug',
        ),
        migrations.RemoveField(
            model_name='purchaseorderitemdata',
            name='purchase_order',
        ),
        migrations.DeleteModel(
            name='PurchaseOrderData',
        ),
        migrations.DeleteModel(
            name='PurchaseOrderItemData',
        ),
    ]
