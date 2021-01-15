# Generated by Django 3.1.3 on 2021-01-12 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0011_stock_ordered_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_Categories', to='stockmgmt.category')),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stockmgmt.subcategory'),
        ),
    ]
