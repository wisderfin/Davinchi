from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot import asyncio_filters
import asyncio
from datetime import datetime
from config import settings
from app.utils import get_all_chat_ids
from app.routers.registration import register_handlers
from app.routers.me import me_handlers
from app.routers.search import search_handlers
from app.routers.edit_profile import edit_profile_handlers
from app.routers.message import message_handlers

bot = AsyncTeleBot(settings.TG_TOKEN, state_storage=StateMemoryStorage())

register_handlers(bot)
message_handlers(bot)
search_handlers(bot)
edit_profile_handlers(bot)
me_handlers(bot)


# отправка сообщения всем пользователям
async def send_daily_message(message: str):
    chat_ids = await get_all_chat_ids()
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Не удалось отправить сообщение в чат {chat_id}: {e}")


# отправка "напоминания" в определеное время
async def scheduler():
    while True:
        now = datetime.now()
        # Проверяем, равны ли текущие часы и минуты 9 и 53 соответственно
        if now.hour == 9 and now.minute == 0:
            print(f"Отправка сообщения в {now.strftime('%Y-%m-%d %H:%M:%S')}")
            await send_daily_message("Вас ждут новые знакомства❤ ️")
            # Ожидаем 60 секунд, чтобы избежать повторного выполнения в течение одной минуты
            await asyncio.sleep(60*60*22*2)
        else:
            # Ожидаем 30 секунд перед следующей проверкой
            await asyncio.sleep(30)


# обработка всех сообщений не попавших в другие обработчики
@bot.message_handler()
async def echo_all(message):
    await bot.reply_to(message, "I don't understand.")


# основной цикл событий
async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    bot.add_custom_filter(asyncio_filters.IsDigitFilter())

    # Запускаем планировщик задач и основной цикл бота параллельно
    await asyncio.gather(
        bot.polling(none_stop=True),  # Запуск основного цикла бота
        scheduler()  # Запуск планировщика задач
    )

if __name__ == '__main__':
    asyncio.run(main())
