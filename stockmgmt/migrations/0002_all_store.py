# Generated by Django 3.1.4 on 2021-01-03 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('Cogon', 'Cogon'), ('Kanangga', 'kanangga'), ('Albuera', 'Albuera'), ('Maasin', 'Maasin')], max_length=100, null=True, verbose_name='Store name')),
            ],
        ),
    ]