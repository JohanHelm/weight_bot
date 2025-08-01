import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dishka import make_async_container
from dishka.integrations.aiogram import (
    AiogramProvider,
    setup_dishka,
)

from config_data.config import Config, load_config
from config_data.logging_settings import configure_logger
from handlers.common import common_router
from handlers.pagination import page_router
from handlers.weighings import weighings_router
from utils.dependencies import MyProvider
from utils.prepare import create_logs_catalogs


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

    dp.include_router(common_router)
    dp.include_router(weighings_router)
    dp.include_router(page_router)

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
