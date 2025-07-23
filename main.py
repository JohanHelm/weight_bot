import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.aiogram import (
    AiogramMiddlewareData,
    AiogramProvider,
    FromDishka,
    inject,
    setup_dishka,
)

from config_data.config import Config, load_config
from config_data.logging_settings import configure_logger
from config_data.initial_settings import PathParams
from handlers.common import main_router
from database.connection import get_db_session
from utils.prepare import create_logs_catalogs
from utils.dependencies import MyProvider

async def main():
    create_logs_catalogs()
    logger = configure_logger(__name__)
    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(
        storage=MemoryStorage(),
    )

    dp.include_router(main_router)

    container = make_async_container(
        MyProvider(config),
        AiogramProvider(),
    )
    setup_dishka(container=container, router=dp, auto_inject=True)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await container.close()
        await bot.session.close()


asyncio.run(main())