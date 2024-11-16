# Generated by Django 5.1.1 on 2024-11-14 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0034_alter_carcolor_options_alter_carmark_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basefilter',
            name='max_eng_v',
            field=models.DecimalField(decimal_places=1, default=6, help_text='не больше какого значения (л)', max_digits=3, verbose_name='максимальный объем двигателя'),
        ),
    ]
