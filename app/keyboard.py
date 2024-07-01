import telebot


# клавиатура гл. меню
def menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.InlineKeyboardButton(text="👤 Мой профиль")  # +
    button2 = telebot.types.InlineKeyboardButton(text="🔎 Поиск")  # +
    button3 = telebot.types.InlineKeyboardButton(text="📝 Установить статус")  # +
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    return keyboard


# клавиатура выбора гендера
def gender_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_m = telebot.types.KeyboardButton(text="♂ М")
    button_w = telebot.types.KeyboardButton(text="♀ Ж")
    keyboard.add(button_m, button_w)
    return keyboard


# клавиатура запроса геолокации
def location_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
    keyboard.add(button)
    return keyboard


# клавиатура выбора статуса
def status_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.InlineKeyboardButton(text='🐕 Собачник')  # +
    button2 = telebot.types.InlineKeyboardButton(text='🗨 Собеседник')  # +
    button3 = telebot.types.InlineKeyboardButton(text='🚫 Не беспокоить')  # +
    button4 = telebot.types.InlineKeyboardButton(text='🔙 Назад')  # +
    keyboard.add(button1, button2, button3)
    keyboard.row(button4)
    return keyboard


# клавиатура поиска(оценки анкет)
def assessment_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.InlineKeyboardButton(text='👍')  # +
    button2 = telebot.types.InlineKeyboardButton(text='👎')  # +
    button3 = telebot.types.InlineKeyboardButton(text="💬 Написать")
    button4 = telebot.types.InlineKeyboardButton(text='🔙 Назад')  # +
    keyboard.add(button1, button2)
    keyboard.row(button3)
    keyboard.row(button4)
    return keyboard


# клавиатура изменения данных профиля
def edit_profile_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.InlineKeyboardButton(text='👤 Сменить имя')
    button2 = telebot.types.InlineKeyboardButton(text='⏳ Сменить возраст')
    button3 = telebot.types.InlineKeyboardButton(text='👫 Сменить пол')
    button4 = telebot.types.InlineKeyboardButton(text='🗺 Сменить локацию')
    button5 = telebot.types.InlineKeyboardButton(text='📷 Сменить фото')
    button6 = telebot.types.InlineKeyboardButton(text='📖 Сменить описание')
    button7 = telebot.types.InlineKeyboardButton(text='🔙 Назад')
    keyboard.row(button1)
    keyboard.row(button2)
    keyboard.row(button3)
    keyboard.row(button4)
    keyboard.row(button5)
    keyboard.row(button6)
    keyboard.row(button7)
    return keyboard
