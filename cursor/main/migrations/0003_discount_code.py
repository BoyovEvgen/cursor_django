# Generated by Django 4.2.1 on 2023-05-29 11:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_order_orderitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount_code',
            fields=[
                ('code', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('expiration_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]