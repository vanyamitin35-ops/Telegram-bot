import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from handlers import router
import config

logging.basicConfig(level=logging.INFO)

dp_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=config.API_TOKEN, default=dp_properties)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

try:
    if __name__ == "__main__":
        asyncio.run(main())
        logging.info("Бот запущен!")
except (KeyboardInterrupt, SystemExit):
    logging.error("Бот остановлен!")

