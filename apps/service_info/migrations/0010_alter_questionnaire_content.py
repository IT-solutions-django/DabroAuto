# Generated by Django 5.1.1 on 2024-10-06 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_info', '0009_alter_questionnaire_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='контент'),
        ),
    ]
