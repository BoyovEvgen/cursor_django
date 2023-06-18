from products.models import Product, ProductImage
from asgiref.sync import sync_to_async

from telegram_bot.models import ProfileTelegram


@sync_to_async
def get_all_products():
    return list(Product.objects.all())


@sync_to_async
def get_product(product_id):
    return Product.objects.get(id=product_id)


@sync_to_async
def get_products_image(product_id):
    image = ProductImage.objects.filter(product=product_id).first()
    return image.image.url

@sync_to_async
def get_create_update_telegram_user(user_id,
                                user_name=None,
                                first_name=None,
                                last_name=None,
                                phone_number=None):
    user, _ = ProfileTelegram.objects.get_or_create(
        id=user_id,
        defaults={
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    if phone_number:
        user.phone = phone_number.lstrip('+')
        user.save()
    return user


@sync_to_async
def add_product_to_profile(profile, product):
    profile.like_products.add(product)


async def save_like(user_id, product_id):
    profile = await get_create_update_telegram_user(user_id=user_id)
    product = await get_product(product_id=product_id)
    await add_product_to_profile(profile, product)
