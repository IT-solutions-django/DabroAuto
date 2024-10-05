from django.db import models
from PIL import Image as Img
from django.core.files.base import ContentFile

from utils.model_fields import SVGAndImageField
import io


class Image(models.Model):
    """Модель описывающая работу с изображениями"""

    image = SVGAndImageField(
        upload_to="images/%Y/%m/%d/",
        verbose_name="изображение",
        help_text="все форматы(кроме svg) конвертируются в webp",
    )

    def save(self, *args, **kwargs):
        if self.image.name.split(".")[-1] != "svg":
            img = Img.open(self.image)

            # Сохраняем изображение в формате WEBP
            img_io = io.BytesIO()
            img.save(img_io, format="WEBP")
            img_io.seek(0)

            self.image = ContentFile(
                img_io.getvalue(),
                name=self.image.name.split(".")[0].split("/")[-1] + ".webp",
            )

        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.name.split("/")[-1]

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"
