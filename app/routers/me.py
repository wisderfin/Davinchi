from telebot.async_telebot import AsyncTeleBot

from app.keyboard import status_keyboard, menu_keyboard, edit_profile_keyboard
from app import redis_utils
from app.utils import get_user


# функция с обработчиками профиля, статуса и возврата
def me_handlers(bot: AsyncTeleBot):
    # обработчик команды показа профиля
    @bot.message_handler(func=lambda mes: mes.text == "👤 Мой профиль")
    async def callback_query(mes):
        user = await get_user(mes.from_user.id)
        try:
            status = redis_utils.get(f'{user.id}')
            status = status if status is not None else 'mute'
        except Exception as _ex:
            status = 'mute'
        if status == 'talcking':
            rus_status = 'Общение'
        elif status == 'teammate':
            rus_status = 'Собачник'
        else:
            rus_status = 'Не беспокоить'
        await bot.send_photo(mes.from_user.id, user.photos, f'Статус: {rus_status}\n'
                                                            f'Имя: {user.name}\n'
                                                            f'Возраст: {user.age}\n'
                                                            f'Пол: {'М' if user.gender else 'Ж'}\n'
                                                            f'Локация: {user.location}\n'
                                                            f'О себе: {user.description}',
                             reply_markup=edit_profile_keyboard())
        redis_utils.set(key=f'{user.id}', value=status)

    # обработчик команды смены статуса
    @bot.message_handler(func=lambda mes: mes.text == '📝 Установить статус')
    async def set_status(mes):

        await bot.send_message(mes.from_user.id, 'Выберите статус', reply_markup=status_keyboard())

    # обработчик команды смены статуса собачник
    @bot.message_handler(func=lambda mes: mes.text == '🐕 Собачник')
    async def set_status_teammeate(mes):
        await bot.send_message(mes.from_user.id, f"Ваш статус: Поиск собачников",
                               reply_markup=menu_keyboard())
        redis_utils.set(key=f'{mes.from_user.id}', value='teammate')

    # обработчик команды смены общения
    @bot.message_handler(func=lambda mes: mes.text == '🗨 Собеседник')
    async def set_status_talcking(mes):
        await bot.send_message(mes.from_user.id, f"Ваш статус: Поиск общения",
                               reply_markup=menu_keyboard())
        redis_utils.set(key=f'{mes.from_user.id}', value='talcking')

    # не беспокоить
    @bot.message_handler(func=lambda mes: mes.text == "🚫 Не беспокоить")
    async def set_status_mute(mes):
        await bot.send_message(mes.from_user.id, f"Ваш статус: Не беспокоить",
                               reply_markup=menu_keyboard())
        redis_utils.set(key=f'{mes.from_user.id}', value='mute')

    # обработчик команды возврата в менюа
    @bot.message_handler(func=lambda mes: mes.text == '🔙 Назад')
    async def callback_query(mes):
        user = await get_user(mes.from_user.id)
        status = redis_utils.get(f'{user.id}')
        if status == 'talcking':
            rus_status = 'Общение'
        elif status == 'teammate':
            rus_status = 'Собачник'
        else:
            rus_status = 'Не беспокоить'
        await bot.send_photo(mes.from_user.id, user.photos, f'Статус: {rus_status}\n'
                                                            f'Имя: {user.name}\n'
                                                            f'Возраст: {user.age}\n'
                                                            f'Пол: {'М' if user.gender else 'Ж'}\n'
                                                            f'Локация: {user.location}\n'
                                                            f'О себе: {user.description}',
                             reply_markup=menu_keyboard())
