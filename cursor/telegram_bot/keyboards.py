from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from products.models import Product
from .utils.async_request_to_db import get_all_products
from cursor.settings import BASE_URL


async def get_inlineKB_list_products():
    products = await get_all_products()  # is_active=True???
    button_list = [InlineKeyboardButton(text=product.title, callback_data=f'product_id_{product.id}')
                   for product in products]
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(*button_list)
    return ikb


def get_KB_main():
    button = KeyboardButton(text='VIEW PRODUCTS')
    button_promo = KeyboardButton(text='GET PROMO CODE')
    button_site = KeyboardButton(text="VIEW WEBSITE")
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=False)
    kb.add(button)
    kb.add(button_promo)
    kb.add(button_site)
    return kb


def get_KB_contact():
    button_phone = KeyboardButton(text='SHARE PHONE', request_contact=True)
    button_stop = KeyboardButton(text='CANCEL')
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             one_time_keyboard=False)
    kb.add(button_phone, button_stop)
    return kb


def get_inlineKB_like_dislike(id_product):
    ikb = InlineKeyboardMarkup(row_width=2)
    ib1 = InlineKeyboardButton(text='❤️', callback_data=f'Key_{id_product}_like')
    ib2 = InlineKeyboardButton(text='👎', callback_data=f'Key_{id_product}_dislike')
    ikb.add(ib1, ib2)
    return ikb




#
# cb = CallbackData('ikb', 'action')


# def get_inlineKB_for_inlineBot():
#     ikb = InlineKeyboardMarkup(row_width=2)
#     ib1 = InlineKeyboardButton(text='Buttun_1', callback_data=cb.new('push_1'))  # callback_data = {'action': 'push_1'}
#     ib2 = InlineKeyboardButton(text='Button_2', callback_data=cb.new('push_2'))
#     ikb.add(ib1, ib2)
#     return ikb