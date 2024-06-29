from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
from app.service import get_city_name
from app.utils import edit_name, edit_age, edit_gender, edit_location, edit_description, edit_photo, get_user
from app.utils import check_banned

from app.keyboard import menu_keyboard, location_keyboard


class EditProfileState(StatesGroup):
    new_name = State()
    new_age = State()
    new_description = State()
    new_photo = State()
    new_location = State()


def edit_profile_handlers(bot: AsyncTeleBot):
    @bot.message_handler(func=lambda mes: mes.text == '👤 Сменить имя')
    async def edit_name_handler(mes):
        await bot.send_message(mes.from_user.id, 'Введите новое имя')
        await bot.set_state(mes.from_user.id, EditProfileState.new_name, mes.from_user.id)

    @bot.message_handler(func=lambda mes: mes.text == "⏳ Сменить возраст")
    async def edit_age_handler(mes):
        await bot.send_message(mes.from_user.id, 'Введите новый возраст')
        await bot.set_state(mes.from_user.id, EditProfileState.new_age, mes.from_user.id)

    @bot.message_handler(func=lambda mes: mes.text == "👫 Сменить пол")
    async def edit_gender_handler(mes):
        user = await get_user(mes.from_user.id)
        gender = not user.gender
        await edit_gender(mes.from_user.id, gender)
        await bot.send_message(mes.from_user.id, 'Пол успешно изменен', reply_markup=menu_keyboard())

    @bot.message_handler(func=lambda mes: mes.text == "🗺 Сменить локацию")
    async def edit_location_handler(mes):
        await bot.send_message(mes.from_user.id, 'Отправьте новую локацию нажав кнопку ниже.',
                               reply_markup=location_keyboard())
        await bot.set_state(mes.from_user.id, EditProfileState.new_location, mes.from_user.id)

    @bot.message_handler(func=lambda mes: mes.text == "📷 Сменить фото")
    async def edit_photo_handler(mes):
        await bot.send_message(mes.from_user.id, 'Отправьте новое фото')
        await bot.set_state(mes.from_user.id, EditProfileState.new_photo, mes.from_user.id)

    @bot.message_handler(func=lambda mes: mes.text == "📖 Сменить описание")
    async def edit_description_handler(mes):
        await bot.send_message(mes.from_user.id, 'Введите нововое описание')
        await bot.set_state(mes.from_user.id, EditProfileState.new_description, mes.from_user.id)

    @bot.message_handler(state=EditProfileState.new_name)
    async def get_new_name(message):
        await edit_name(id=message.from_user.id, new_name=message.text)
        await bot.send_message(message.from_user.id, f'Имя успешно изменено', reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=EditProfileState.new_age, is_digit=True)
    async def get_new_age(message):
        await edit_age(id=message.from_user.id, new_age=int(message.text))
        await bot.send_message(message.from_user.id, f'Возраст успешно изменен', reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=EditProfileState.new_age, is_digit=False)
    async def new_age_incorrect(message):
        await bot.send_message(message.chat.id, 'Возраст некорректен, попробуй снова.')

    @bot.message_handler(state=EditProfileState.new_location, content_types=['location'])
    async def get_new_location(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            location = await get_city_name(latitude=message.location.latitude, longitude=message.location.longitude)
        await edit_location(message.from_user.id, location)
        await bot.send_message(message.from_user.id, 'Локация успешно изменена', reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=EditProfileState.new_photo, content_types=['photo'])
    async def get_new_photo(message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            photo_id = message.photo[-1].file_id
        await edit_photo(message.from_user.id, photo_id)
        await bot.send_message(message.from_user.id, 'Фото профиля, успешно изменено',
                               reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=EditProfileState.new_description)
    async def get_new_description(message):
        await edit_description(id=message.from_user.id, new_description=message.text)
        await bot.send_message(message.from_user.id, f'Описание успешно изменено', reply_markup=menu_keyboard())
        await bot.delete_state(message.from_user.id, message.chat.id)
