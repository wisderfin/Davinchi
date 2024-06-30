from telebot.async_telebot import AsyncTeleBot
import telebot
from app import redis_utils
from app.utils import get_user, get_users
from random import choice
from app.keyboard import assessment_keyboard


from random import choice


def search_handlers(bot: AsyncTeleBot):
    @bot.message_handler(func=lambda mes: mes.text == '👎' or mes.text == '🔎 Поиск')
    async def callback_query(mes):
        status = redis_utils.get(key=f'{mes.from_user.id}')
        if status == 'mute':
            redis_utils.set(key=f'{mes.from_user.id}', value='talcking')
            status = 'talcking'

        user = await get_user(mes.from_user.id)
        search_gender = not user.gender if status != 'teammate' else None
        users = await get_users(location=user.location, age=user.age, gender=search_gender)

        if users:
            attempts = 0
            max_attempts = 10  # Максимальное количество попыток для поиска подходящего пользователя

            while attempts < max_attempts:
                rand_user = choice(users)
                other_status = redis_utils.get(key=f'{rand_user.id}')

                if rand_user.id != user.id and status == other_status:
                    if status == 'talcking':
                        rus_status = 'Общение'
                    elif status == 'teammate':
                        rus_status = 'Тимейтинг'
                    else:
                        rus_status = 'Не беспокоить'
                    await bot.send_photo(
                        mes.from_user.id,
                        rand_user.photos,
                        f'Статус: {rus_status}\n'
                        f'Имя: {rand_user.name}\n'
                        f'Возраст: {rand_user.age}\n'
                        f'Пол: {"М" if rand_user.gender else "Ж"}\n'
                        f'Локация: {rand_user.location}\n'
                        f'О себе: {rand_user.description}',
                        reply_markup=assessment_keyboard()
                    )
                    redis_utils.set(key=f'last:{mes.from_user.id}', value=rand_user.id)
                    return

                attempts += 1

            await bot.send_message(mes.from_user.id, f'Активных людей со статусом {status} не нашлось, '
                                                     f'попробуй сменить статус или подожди.')
        else:
            await bot.send_message(mes.from_user.id, f'Активных людей со статусом {status} не нашлось, '
                                                     f'попробуй сменить статус или подожди.')

    @bot.message_handler(func=lambda mes: mes.text == '👍')
    async def callback_like(mes):
        liked_user = int(redis_utils.get(key=f'last:{mes.from_user.id}'))
        try:
            list_other_user = redis_utils.get_json(key=f'liked:{liked_user}')
        except Exception as _ex:
            list_other_user = []

        try:
            list_current_user = redis_utils.get_json(key=f'liked:{mes.from_user.id}')
        except Exception as _ex:
            list_current_user = []

        # Если list_other_user или list_current_user равны None, присваиваем им пустой список
        if list_other_user is None:
            list_other_user = []

        if list_current_user is None:
            list_current_user = []

        # Проверяем, есть ли у лайкнутого лайки (не свои)
        if not list_other_user:
            redis_utils.set_json(key=f'liked:{liked_user}', value=[mes.from_user.id])

        # Если лайкнувший не в списке лайкнутых - добавляем
        elif mes.from_user.id not in list_other_user:
            list_other_user.append(mes.from_user.id)
            redis_utils.set_json(key=f'liked:{liked_user}', value=list_other_user)

        # Если лайкнувший в списке у лайкнутого
        if liked_user in list_current_user:
            other_user = await get_user(int(liked_user))
            await bot.send_message(mes.from_user.id, f'У вас мэтч! Вот контакт: @{other_user.account}')
            await bot.send_message(other_user.id, f'Вас только что лайкнул другой пользователь и это взаимно! '
                                                  f'Вот контакт: @{mes.from_user.username}')
        else:
            await bot.send_message(mes.from_user.id, f'Вы получите уведомления в случае мэтча')

        await callback_query(mes)

