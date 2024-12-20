# Generated by Django 5.1.1 on 2024-10-20 07:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clip', '0003_alter_clip_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClipPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='максимальная длина 255 символов', max_length=255, unique=True, verbose_name='название')),
                ('url', models.TextField(help_text='ссылка в формате http/...', verbose_name='ссылка')),
                ('playlists', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, help_text='плейлисты где расположены клипы, несколько значений разделяются запятой', null=True, size=None, verbose_name='плейлисты')),
            ],
            options={
                'verbose_name': 'площадка с клипами',
                'verbose_name_plural': 'площадки с клипами',
            },
        ),
    ]
