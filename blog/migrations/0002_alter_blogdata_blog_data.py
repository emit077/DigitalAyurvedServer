# Generated by Django 3.2 on 2023-05-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdata',
            name='blog_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
