# Generated by Django 5.1.1 on 2024-10-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_alter_reviewauthor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewlocation',
            name='count_upload',
            field=models.PositiveIntegerField(default=0, help_text='больше нуля', verbose_name='количество для скачивания'),
        ),
    ]
