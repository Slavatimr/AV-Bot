import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers import command_handler, step1_handler, step2_handler, search_handler, link_handler
from config import TOKEN
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(command_handler.router, step1_handler.router, step2_handler.router, search_handler.router,
                       link_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
