# Generated by Django 5.1.1 on 2024-10-09 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_carkpp_carpriv'),
        ('catalog', '0029_alter_basefilter_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(default=994, on_delete=django.db.models.deletion.PROTECT, related_name='car', to='catalog.carcolor', verbose_name='цвет'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='eng_v',
            field=models.DecimalField(decimal_places=1, default=0, help_text='значение в литрах', max_digits=3, verbose_name='объем двигателя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='kpp',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='car', to='car.carkpp', verbose_name='КПП'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='kuzov',
            field=models.CharField(default=1, help_text='максимальная длина - 100 символов', max_length=100, verbose_name='кузов'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='priv',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='car', to='car.carpriv', verbose_name='привод'),
            preserve_default=False,
        ),
    ]