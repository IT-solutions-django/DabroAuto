# Generated by Django 5.1.1 on 2024-10-06 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_remove_carmodel_country_manufacturing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basefilter',
            name='country_manufacturing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
        ),
        migrations.AlterField(
            model_name='carcolor',
            name='country_manufacturing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
        ),
        migrations.AlterField(
            model_name='carmark',
            name='country_manufacturing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
        ),
        migrations.AlterField(
            model_name='carpriv',
            name='country_manufacturing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
        ),
    ]
