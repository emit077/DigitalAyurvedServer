# Generated by Django 4.0.5 on 2022-06-28 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorsdata',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='doctorsdata',
            name='payment_id',
        ),
    ]