from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
import telebot
from app.service import get_city_name
from app.utils import create_user, get_user

from app import redis_utils
from app.keyboard import menu_keyboard, gender_keyboard, location_keyboard


def register_handlers(bot: AsyncTeleBot):
    @bot.message_handler(commands=['ban'])
    async def send_welcome(message):
        user = await get_user(message.from_user.id)
        if user.admin:
            last = redis_utils.get(f'last:{message.from_user.id}')
            
        else:
            await bot.send_message(message.from_user.id, 'У вас недостаточно прав')
