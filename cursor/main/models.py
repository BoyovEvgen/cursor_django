from django.db import models
from django.conf import settings
from products.models import Product
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


class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    total_price = models.IntegerField()

    def __str__(self):
        return str(self.id) + " " + self.address


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return str(self.order.id) + " " + self.product.title