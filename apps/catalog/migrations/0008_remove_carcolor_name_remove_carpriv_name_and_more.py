# Generated by Django 5.1.1 on 2024-10-06 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_carpriv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carcolor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='carpriv',
            name='name',
        ),
        migrations.AddField(
            model_name='carcolor',
            name='country_manufacturing',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carmark',
            name='country_manufacturing',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carmodel',
            name='country_manufacturing',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carpriv',
            name='country_manufacturing',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basefilter',
            name='country_manufacturing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='catalog.country', verbose_name='страна производства'),
        ),
    ]