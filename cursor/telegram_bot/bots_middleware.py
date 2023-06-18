from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher
from asgiref.sync import sync_to_async

from telegram_bot.utils.async_request_to_db import get_create_update_telegram_user


class CheckUserMiddleware(BaseMiddleware):

    async def on_process_message(self, message: types.Message,  data: dict):
        user_id = message.from_user.id
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user = await get_create_update_telegram_user(user_id, user_name, first_name, last_name)
        await self.print_user_info(user.id)

    @staticmethod
    async def print_user_info(user_id):
        print('Middleware prints users ID: ', user_id)
