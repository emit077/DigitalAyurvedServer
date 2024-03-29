# Generated by Django 3.2.7 on 2024-01-30 17:00

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0006_auto_20221205_1314'),
        ('drugs', '0017_auto_20231230_1559'),
        ('master', '0007_auto_20231212_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('order_date', models.DateTimeField(blank=True, null=True)),
                ('order_total', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=11, null=True)),
                ('transaction_type', models.CharField(choices=[('Purchase Order', 'Purchase Order'), ('Sales Order', 'Sales Order'), ('Shrink Item', 'Shrink Item'), ('Archive Item', 'Archive Item'), ('Expired Item', 'Expired Item')], max_length=20, verbose_name='transaction_type')),
                ('comment', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='patient.patientsdata')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_vendor', to='master.mastervendordata')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetailsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=255)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=11)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_drug', to='drugs.drugdata')),
                ('order_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_out_item_data', to='inventory.orderdata')),
            ],
        ),
    ]
