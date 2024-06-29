from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot import asyncio_filters
import telebot
import asyncio

from config import settings
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


@bot.message_handler()
async def echo_all(message):
    await bot.reply_to(message, "I don't understand.")


async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    bot.add_custom_filter(asyncio_filters.IsDigitFilter())
    await bot.polling(none_stop=True)


if __name__ == '__main__':
    asyncio.run(main())
