# Generated by Django 5.1.1 on 2024-11-05 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0012_review_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='text',
        ),
    ]
