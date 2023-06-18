from django.core.management.base import BaseCommand
from telegram_bot.bot_methods import dispatcher
import asyncio
from telegram_bot.bot_methods import start, get_all_product


class Command(BaseCommand):
    help = 'Starts the Telegram bot polling'

    def handle(self, *args, **options):
        dispatcher.register_message_handler(start, commands=['start'])
        dispatcher.register_message_handler(get_all_product, commands=['view_all_products'])

        loop = asyncio.get_event_loop()
        try:
            loop.create_task(dispatcher.start_polling())
            loop.run_forever()
        finally:
            loop.stop()
            loop.close()
