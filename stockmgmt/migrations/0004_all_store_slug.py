# Generated by Django 3.1.4 on 2021-01-03 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0003_all_store_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_store',
            name='slug',
            field=models.SlugField(default='na', unique=True),
        ),
    ]
