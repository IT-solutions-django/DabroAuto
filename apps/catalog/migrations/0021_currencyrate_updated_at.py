# Generated by Django 5.1.1 on 2024-10-08 04:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_alter_currencyrate_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencyrate',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата обновления'),
            preserve_default=False,
        ),
    ]