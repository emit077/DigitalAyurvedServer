# Generated by Django 3.2.7 on 2023-04-26 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_masterbranddata_masterformulareferencedata_masterpackagingtypedata_mastervendordata'),
        ('drugs', '0006_auto_20230426_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugdata',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drug_brand', to='master.masterbranddata'),
        ),
    ]
