# Generated by Django 5.1.1 on 2024-09-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.CharField(help_text='формат данных: 8 августа 2024', max_length=100, verbose_name='дата добавления отзыва'),
        ),
    ]
