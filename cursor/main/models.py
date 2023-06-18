from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
# from products.models import Product
import os


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Add related_name argument to fields
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.username


User = get_user_model()


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


class Discount_code(models.Model):
    code = models.CharField(max_length=12, primary_key=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    for_user_phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.discount) + "%, expiration_date: " + str(self.expiration_date) + f' for User: {self.for_user_phone}'
