# Generated by Django 3.1.3 on 2021-01-21 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0019_auto_20210118_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_record',
            name='reoder_level',
            field=models.IntegerField(default=0, verbose_name='Reorder level'),
        ),
    ]
