# Generated by Django 5.1.1 on 2024-11-05 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0011_reviewlocation_count_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.TextField(default='', verbose_name='текст отзыва'),
            preserve_default=False,
        ),
    ]
