# Generated by Django 4.0.5 on 2022-06-28 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(blank=True, max_length=70, null=True)),
                ('degree', models.CharField(max_length=255, null=True)),
                ('medical_reg_no', models.CharField(max_length=150)),
                ('designation', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=70, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=70, null=True)),
                ('payment_date', models.DateTimeField(blank=True, max_length=70, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
