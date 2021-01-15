# Generated by Django 3.1.3 on 2021-01-13 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0014_auto_20210113_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_store',
            name='name',
            field=models.CharField(blank=True, choices=[('Cogon', 'Cogon'), ('Kanangga', 'kanangga'), ('Maasin', 'Maasin'), ('BODEGA', 'BODEGA'), ('HILONGOS', 'HILONGOS'), ('ALANG-ALANG', 'ALANG-ALANG'), ('BOHOL', 'BOHOL')], max_length=100, null=True, verbose_name='Store name'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='issue_by',
            field=models.CharField(blank=True, choices=[('Cogon', 'Cogon'), ('Kanangga', 'kanangga'), ('Maasin', 'Maasin'), ('BODEGA', 'BODEGA'), ('HILONGOS', 'HILONGOS'), ('ALANG-ALANG', 'ALANG-ALANG'), ('BOHOL', 'BOHOL')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='issue_to',
            field=models.CharField(blank=True, choices=[('Cogon', 'Cogon'), ('Kanangga', 'kanangga'), ('Maasin', 'Maasin'), ('BODEGA', 'BODEGA'), ('HILONGOS', 'HILONGOS'), ('ALANG-ALANG', 'ALANG-ALANG'), ('BOHOL', 'BOHOL')], max_length=50, null=True),
        ),
    ]