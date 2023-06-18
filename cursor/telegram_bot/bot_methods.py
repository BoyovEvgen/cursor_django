import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from cursor.settings import TOKEN_TELEGRAM, BASE_URL
from api.serializers import OrderSerializer
from .utils.async_request_to_db import get_all_products, get_products_image, get_product, \
    get_create_update_telegram_user, save_like
from .keyboards import get_inlineKB_list_products, get_KB_main, get_inlineKB_like_dislike, get_KB_contact
from .bots_middleware import CheckUserMiddleware
from django.contrib.auth import get_user_model

from .utils.individual_promocode import create_promo_code

User = get_user_model()


bot = Bot(TOKEN_TELEGRAM)
storage = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=storage)
dispatcher.middleware.setup(CheckUserMiddleware())


class StateMachine(StatesGroup):
    waiting_photo = State()


def serialize_order_send_message(order):
    order = OrderSerializer(order).data
    asyncio.run(send_message(order))


async def send_message(order):
    await bot.send_message(chat_id=-765649794, text=order)


async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Hello, {message.from_user.first_name} {message.from_user.last_name}\n"
                                f"Your ID {message.from_user.id}",
                           reply_markup=get_KB_main())
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def get_all_product(message: types.Message):
    products = await get_all_products()

    for product in products:
        image_url = BASE_URL + await get_products_image(product.id)
        print(image_url)
        caption = f'Product: {product.title}\n' \
                  f'Price: {product.price} $\n' \
                  f'ID: {product.id}'
        await bot.send_photo(chat_id=message.chat.id,
                             photo=image_url,
                             caption=caption)


@dispatcher.message_handler(filters.Text(equals="VIEW PRODUCTS"))
async def get_list_products(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id,
                           text='AVAILABLE PRODUCTS',
                           reply_markup=await get_inlineKB_list_products()
                           )


@dispatcher.message_handler(filters.Text(equals="GET PROMO CODE"))
async def get_promo_code(message: types.Message,  state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await StateMachine.waiting_photo.set()
    current_state = await state.get_state()  # додати пперевірку ID
    await bot.send_message(chat_id=message.from_user.id,
                           text="To create an individual discount, I need your phone number."
                                "\nPlease click <SHARE PHONE>", reply_markup=get_KB_contact())
    print(current_state)


@dispatcher.message_handler(filters.Text(equals="CANCEL"), state=StateMachine.waiting_photo)
async def contact_handler(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.from_user.id, text='Ок', reply_markup=get_KB_main())
    await state.reset_state()


@dispatcher.message_handler(content_types=types.ContentTypes.CONTACT, state=StateMachine.waiting_photo)
async def contact_handler(message: types.Message, state: FSMContext):
    contact = message.contact
    print(contact.phone_number)
    await get_create_update_telegram_user(user_id=contact.user_id,
                                    first_name=contact.first_name,
                                    last_name=contact.last_name,
                                    phone_number=contact.phone_number)
    promocode = await create_promo_code(contact.phone_number)
    text = f'Individual Promo code for you: {promocode.code}\n' \
           f'Discount: {promocode.discount}%\n' \
           f'Expiration_date: {promocode.expiration_date}\n' \
           f'Use it on the website: \n{BASE_URL}'

    await bot.send_message(chat_id=message.from_user.id,
                           text=text,
                           reply_markup=get_KB_main())
    await state.reset_state()


@dispatcher.callback_query_handler(lambda callback_query: callback_query.data.startswith('product_id'))
async def product_callback(callback: types.CallbackQuery):
    product_id = callback.data.split('_')[-1]
    product = await get_product(product_id)
    image_url = BASE_URL + await get_products_image(product.id)
    caption = f'Product: {product.title}\n' \
              f'Price: {product.price} $\n' \
              f'ID: {product.id}'
    await bot.send_photo(chat_id=callback.message.chat.id,
                         photo=image_url,
                         caption=caption,
                         reply_markup=get_inlineKB_like_dislike(product.id))


@dispatcher.callback_query_handler(lambda callback_query: callback_query.data.startswith('Key'))
async def vote_callback(callback: types.CallbackQuery):
    _, product_id, like = callback.data.split('_')
    if like == 'like':
        await callback.answer(text='Дякую за твою вподобайку!')  # відображає у стікері
        await save_like(user_id=callback.from_user.id, product_id=product_id)

    await callback.answer(text='FACK YOU!', show_alert=True)  # відображає у вікні


@dispatcher.message_handler(filters.Text(equals="VIEW WEBSITE"))
async def contact_handler(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.from_user.id, text=f'Welcome to website:\n{BASE_URL}')
