# Generated by Django 3.1.3 on 2021-01-04 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0008_sold_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transit_Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_items', models.IntegerField(default=0)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stockmgmt.stock')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stockmgmt.all_store')),
            ],
        ),
    ]