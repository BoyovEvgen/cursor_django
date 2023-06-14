import asyncio

from aiogram import Bot, Dispatcher, types
from cursor.settings import TOKEN_TELEGRAM, BASE_URL
from api.serializers import OrderSerializer
from products.models import Product, ProductImage
from asgiref.sync import sync_to_async


bot = Bot(TOKEN_TELEGRAM)
dispatcher = Dispatcher(bot=bot)


def serialize_order_send_message(order):
    order = OrderSerializer(order).data
    asyncio.run(send_message(order))


async def send_message(order):
    await bot.send_message(chat_id=-765649794, text=order)


async def start(message: types.Message):
    await message.reply(f"Hello, {message.from_user.first_name} {message.from_user.last_name} \n"
                        f"Your ID {message.from_user.id}")


@sync_to_async
def get_all_products_async():
    return list(Product.objects.all())


@sync_to_async
def get_products_image(product_id):
    image = ProductImage.objects.filter(product=product_id).first()
    return image.image.url


async def get_all_product(message: types.Message):
    products = await get_all_products_async()

    for product in products:
        image_url = BASE_URL + await get_products_image(product.id)
        print(image_url)
        caption = f'Product: {product.title}\n' \
                  f'Price: {product.price} $\n' \
                  f'ID: {product.id}'
        await bot.send_photo(chat_id=message.chat.id,
                             photo=image_url,
                             caption=caption)

