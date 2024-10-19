# Generated by Django 5.1.1 on 2024-09-27 01:10

from django.db import migrations
import apps.image.models


class Migration(migrations.Migration):

    dependencies = [
        ("image", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=apps.image.models.SVGAndImageField(
                help_text="все форматы(кроме svg) конвертируются в webp",
                upload_to="images/%Y/%m/%d/",
                verbose_name="изображение",
            ),
        ),
    ]