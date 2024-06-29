from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
import telebot
from app.service import get_city_name
from app.utils import create_user, get_user

from app import redis_utils
from app.keyboard import menu_keyboard, gender_keyboard, location_keyboard


class RegisterState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    description = State()
    photo = State()
    location = State()


def register_handlers(bot: AsyncTeleBot):
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        user = await get_user(message.from_user.id)
        if user is None:
            await bot.send_message(message.from_user.id, 'Привет, как тебя зовут?')
            await bot.set_state(message.from_user.id, RegisterState.name, message.chat.id)
        else:
            await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы', reply_markup=menu_keyboard())

    @bot.message_handler(state=RegisterState.name)
    async def get_name(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
        await bot.reply_to(message, 'Сколько тебе лет?')
        await bot.set_state(message.from_user.id, RegisterState.age, message.chat.id)

    @bot.message_handler(state=RegisterState.age, is_digit=True)
    async def get_age(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text

        await bot.send_message(message.chat.id, "Укажите свой пол.", reply_markup=gender_keyboard())
        await bot.set_state(message.from_user.id, RegisterState.gender, message.chat.id)

    @bot.message_handler(state=RegisterState.age, is_digit=False)
    async def age_incorrect(message):
        await bot.send_message(message.chat.id, 'Возраст некорректен, попробуй снова.')

    @bot.message_handler(state=RegisterState.gender)
    async def get_gender(message):
        if message.text in ['♂ М', '♀ Ж']:
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['gender'] = message.text[-1]
            await bot.send_message(message.chat.id, "Расскажите о себе",
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
            await bot.set_state(message.from_user.id, RegisterState.description, message.chat.id)
        else:
            await bot.send_message(message.chat.id, 'Неправильный выбор, укажите свой пол снова.')

    @bot.message_handler(state=RegisterState.description)
    async def get_description(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['description'] = message.text
        await bot.send_message(message.chat.id, "Отправьте своё фото",
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        await bot.set_state(message.from_user.id, RegisterState.photo, message.chat.id)

    @bot.message_handler(content_types=['photo'], state=RegisterState.photo)
    async def handle_photo(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_id'] = message.photo[-1].file_id

        await bot.send_message(message.chat.id, "Пожалуйста, отправьте своё местоположение, нажав на кнопку ниже.",
                               reply_markup=location_keyboard())
        await bot.set_state(message.from_user.id, RegisterState.location, message.chat.id)

    @bot.message_handler(content_types=['location'], state=RegisterState.location)
    async def get_location(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            location = await get_city_name(latitude=message.location.latitude, longitude=message.location.longitude)
            data['location'] = location
            await bot.send_photo(message.chat.id,
                                 data['photo_id'], f'Имя: {data["name"]}\nВозраст: {data["age"]}\n'
                                                   f'Пол: {data["gender"]}\n'
                                                   f'Локация: {data["location"]}\n'
                                                   f'О себе: {data["description"]}',
                                 reply_markup=menu_keyboard())
            user_data = {
                'id': message.from_user.id,
                'name': data['name'],
                'description': data['description'],
                'gender': True if data['gender'] == 'М' else False,
                'age': int(data['age']),
                'location': data['location'],
                'photos': data['photo_id'],
                'account': message.from_user.username
            }
        await create_user(data=user_data)
        redis_utils.set(key=f'{user_data['id']}', value='talcking')
        await bot.send_message(message.from_user.id, 'Вы успешно зарегистрированы', reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)


