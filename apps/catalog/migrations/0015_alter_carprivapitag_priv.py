# Generated by Django 5.1.1 on 2024-10-07 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_remove_carpriv_country_manufacturing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carprivapitag',
            name='priv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_tags', to='catalog.carpriv', verbose_name='привод'),
        ),
    ]
