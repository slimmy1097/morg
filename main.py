import asyncio
import random
import time

import asyncio
from aiogram import Bot, Dispatcher

from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

from handlers_m import handlers
from db.db_work import init_main
from config import settings, logger


async def main():
    logger.info('START BOT')
    logger.info('Инициализация базы данных')
    await init_main()

    logger.info('инициализируем бот и диспетчер')
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    logger.info('регистриуем роутеры в диспетчере')
    dp.include_router(handlers.router)

    logger.info('удаляем апдейты, запуск polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
