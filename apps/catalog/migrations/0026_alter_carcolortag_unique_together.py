# Generated by Django 5.1.1 on 2024-10-08 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_alter_carcolortag_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carcolortag',
            unique_together={('name', 'color', 'country_manufacturing')},
        ),
    ]
