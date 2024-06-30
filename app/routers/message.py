from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup

from app.service import get_city_name
from app.utils import edit_name, edit_age, edit_gender, edit_location, edit_description,edit_photo, get_user
from app import redis_utils
from app.keyboard import menu_keyboard, assessment_keyboard
from app.routers.search import callback_like, callback_search


class MessageState(StatesGroup):
    send = State()


def message_handlers(bot: AsyncTeleBot):
    @bot.message_handler(func=lambda mes: mes.text == '💬 Написать')
    async def callback_query(mes):
        last_id = redis_utils.get(key=f'last:{mes.from_user.id}')
        last_user = await get_user(int(last_id))
        await bot.send_message(mes.from_user.id, f'Введите сообщение для {last_user.name}')
        await bot.set_state(mes.from_user.id, MessageState.send, mes.chat.id)

    @bot.message_handler(state=MessageState.send)
    async def send_message(mes):
        if mes.text == '🔙 Назад':
            await bot.send_message(mes.from_user.id, 'Отправка отменена', reply_markup=menu_keyboard())
            await bot.delete_state(mes.from_user.id, mes.chat.id)
            return

        last_id = redis_utils.get(key=f'last:{mes.from_user.id}')
        await bot.send_message(last_id, f'Сообщение от пользователя: '
                                        f'{mes.from_user.username}\n{"\t"*5}{mes.text}')
        await bot.send_message(mes.from_user.id, 'Сообщение доставлено', reply_markup=assessment_keyboard())
        await callback_like(mes, bot)
        await bot.delete_state(mes.from_user.id, mes.chat.id)



