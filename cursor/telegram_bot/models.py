from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from products.models import Product


class ProfileTelegram(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(null=True, blank=True, max_length=50)
    first_name = models.CharField(null=True, blank=True, max_length=50)
    last_name = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=20)
    like_products = models.ManyToManyField(Product, blank=True, related_name="telegram_users_like")

    class Meta:
        verbose_name = 'Telegram profile'
        verbose_name_plural = 'Telegram profiles'

    def __str__(self):
        return f'ID: {self.id} {self.first_name} {self.last_name}'


class DiscontSetings(models.Model):
    name = models.CharField(max_length=20, default='Telegram')
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=False)
    days_of_validity = models.IntegerField(null=True, blank=True)
