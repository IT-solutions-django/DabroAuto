# Generated by Django 5.1.1 on 2024-10-08 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_alter_carmark_name_alter_carmark_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carcolortag',
            unique_together={('name', 'color')},
        ),
        migrations.RemoveField(
            model_name='carcolortag',
            name='country_manufacturing',
        ),
    ]
