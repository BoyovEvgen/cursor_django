import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from cursor.settings import TOKEN_TELEGRAM
from api.serializers import OrderSerializer

bot = Bot(TOKEN_TELEGRAM)
# dispatcher = Dispatcher(bot=bot)


def serialize_send_message(order):
    order = OrderSerializer(order).data
    asyncio.run(send_message(order))


async def send_message(order):
    await bot.send_message(chat_id=-765649794, text=order)