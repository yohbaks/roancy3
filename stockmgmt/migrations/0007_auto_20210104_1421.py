# Generated by Django 3.1.3 on 2021-01-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0006_auto_20210104_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_record',
            name='remaining_items',
            field=models.IntegerField(default=0),
        ),
    ]