# Generated by Django 3.2.7 on 2023-12-12 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0009_purchaseorderdata_purchaseorderitemdata'),
        ('master', '0006_matervendordata'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MaterFrequencyData',
            new_name='MasterBrandData',
        ),
        migrations.RenameModel(
            old_name='MaterBrandData',
            new_name='MasterFrequencyData',
        ),
        migrations.RenameModel(
            old_name='MaterPackagingData',
            new_name='MasterInstructionData',
        ),
        migrations.RenameModel(
            old_name='MaterInstructionData',
            new_name='MasterPackagingData',
        ),
        migrations.RenameModel(
            old_name='MaterReferenceData',
            new_name='MasterReferenceData',
        ),
        migrations.RenameModel(
            old_name='MaterVendorData',
            new_name='MasterVendorData',
        ),
        migrations.RenameField(
            model_name='masterbranddata',
            old_name='frequency',
            new_name='brand_name',
        ),
        migrations.RenameField(
            model_name='masterfrequencydata',
            old_name='brand_name',
            new_name='frequency',
        ),
        migrations.RenameField(
            model_name='masterinstructiondata',
            old_name='packaging_type',
            new_name='instruction',
        ),
        migrations.RenameField(
            model_name='masterpackagingdata',
            old_name='instruction',
            new_name='packaging_type',
        ),
    ]