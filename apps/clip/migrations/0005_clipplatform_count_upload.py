# Generated by Django 5.1.1 on 2024-10-20 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip', '0004_clipplatform'),
    ]

    operations = [
        migrations.AddField(
            model_name='clipplatform',
            name='count_upload',
            field=models.PositiveIntegerField(default=0, help_text='больше нуля', verbose_name='количество для скачивания'),
        ),
    ]
