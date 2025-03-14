# pip install telethon

import asyncio
from aiogram import Bot, Dispatcher
from handlers_m import handlers
from db.db_work import init_main
from config import Config, load_config, logger


async def main():

    logger.info('Загрузка конфига в переменную config')
    config: Config = load_config()

    logger.info('Инициализация базы данных')
    await init_main()

    logger.info('инициализируем бот и диспетчер')
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    logger.info('регистриуем роутеры в диспетчере')
    dp.include_router(handlers.router)

    logger.info('удаляем апдейты, запуск polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
