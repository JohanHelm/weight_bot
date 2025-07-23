import asyncio
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, ContentType, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka


# from filters.my_filters import LabEmployee
from lexicon.reply_texts import (create_hello_msg,
                                 get_user_names,
                                 great_new_user
                                 )
# from keyboards.markups import main_markup, back_markup, set_params_markup
from config_data.logging_settings import configure_logger
from config_data.config import Config, TgBot
from database.dao.user_dao import UserAccessUserDAO
# from config_data.initial_settings import PlotParams
# from database.db_client import Database
# from services.plot_service import create_plot
# from services.sensor import get_temp_hum
# from utils.helpers import edit_message_media, correct_temp_setting, correct_hum_setting
# from states.fsm import FSMSettingsForm


logger = configure_logger(__name__)
main_router = Router()


@main_router.message(CommandStart())
async def start(msg: Message,
                bot_config: FromDishka[TgBot],
                user_dao: FromDishka[UserAccessUserDAO]
                ):
    logger.info(f"User {get_user_names(msg)} have start the bot")
    user = user_dao.get_one("telegram_id", msg.from_user.id)
    if user is None:
        reply_msg = great_new_user(msg)
        user_dao.add_one({"username": get_user_names(msg), "telegram_id": msg.from_user.id})
    else:
        reply_msg = create_hello_msg(msg)

    await msg.bot.send_photo(chat_id=msg.from_user.id,
                             photo=bot_config.bot_pic,
                             caption=reply_msg,
                             # reply_markup=main_markup,
                             )





# Этот хэндлер будет срабатывать на отправку боту фотоF.content_type == ContentType.PHOTO
@main_router.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    print(message.photo)
    print(message.photo[-1].file_id)
    await message.reply_photo(message.photo[-1].file_id)
