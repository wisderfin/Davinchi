from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters
import telebot
import asyncio

from config import settings
from app.service import get_city_name
from app.utils import create_user

bot = AsyncTeleBot(settings.TG_TOKEN, state_storage=StateMemoryStorage())


class MyStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    description = State()
    photo = State()
    location = State()


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, f'Привет, как тебя зовут?')
    await bot.set_state(message.from_user.id, MyStates.name, message.chat.id)


@bot.message_handler(state=MyStates.name)
async def get_name(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    await bot.reply_to(message, f'Сколько тебе лет?')
    await bot.set_state(message.from_user.id, MyStates.age, message.chat.id)


@bot.message_handler(state=MyStates.age, is_digit=True)
async def get_age(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_m = telebot.types.KeyboardButton(text="М")
    button_w = telebot.types.KeyboardButton(text="Ж")
    keyboard.add(button_m, button_w)
    await bot.send_message(message.chat.id, "Укажите свой пол.",
                           reply_markup=keyboard)
    await bot.set_state(message.from_user.id, MyStates.gender, message.chat.id)


@bot.message_handler(state=MyStates.age, is_digit=False)
async def age_incorrect(message):
    await bot.send_message(message.chat.id, 'Возраст не коректен, попробуй снова.')


@bot.message_handler(state=MyStates.gender)
async def get_gender(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['gender'] = message.text

    await bot.send_message(message.chat.id, "Расскажите о себе",
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    await bot.set_state(message.from_user.id, MyStates.description, message.chat.id)


@bot.message_handler(state=MyStates.description)
async def get_description(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['description'] = message.text
    await bot.send_message(message.chat.id, "Отправьте своё фото",
                           reply_markup=telebot.types.ReplyKeyboardRemove())
    await bot.set_state(message.from_user.id, MyStates.photo, message.chat.id)


@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['photo_id'] = message.photo[-1].file_id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button)
    await bot.send_message(message.chat.id, "Пожалуйста, отправьте своё местоположение, нажав на кнопку ниже.",
                           reply_markup=keyboard)
    await bot.set_state(message.from_user.id, MyStates.location, message.chat.id)


@bot.message_handler(content_types=['location'], state=MyStates.location)
async def get_location(message):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        location = await get_city_name(latitude=message.location.latitude, longitude=message.location.longitude)
        data['location'] = location
        await bot.send_photo(message.chat.id, data['photo_id'], f'Имя: {data["name"]}\nВозраст: {data["age"]}\n'
                                                                f'Пол: {data["gender"]}\nЛокация: {data["location"]}',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
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
    await bot.send_message(message.from_user.id, 'Вы успешно зарегестрированы')


@bot.message_handler()
async def echo_all(message):
    await bot.reply_to(message, "I don't understand.")


async def main():
    await bot.polling(none_stop=True)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.IsDigitFilter())

if __name__ == '__main__':
    asyncio.run(main())
