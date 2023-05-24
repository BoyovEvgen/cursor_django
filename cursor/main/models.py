from django.db import models
from django.conf import settings
import os

# Create your models here.


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class SliderItem(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        file_name = os.path.basename(self.image.name)
        media_path = os.path.relpath(settings.MEDIA_ROOT, settings.BASE_DIR)  # достає папку в яку зберігаютьс медиа
        link = os.path.join(media_path, 'uploads', file_name)  #збирає шлях, який потім rout передає в html
        self.link = link
        super().save(*args, **kwargs)
