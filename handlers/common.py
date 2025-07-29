import random
from _datetime import datetime, UTC
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, ContentType, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka

from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (create_hello_msg,
                                 get_user_names,
                                 help_msg,
                                 create_track_weight_msg,
                                 create_not_enough_data_msg,
                                 )

from markups.keyboards import main_keyboard, back_keyboard
from config_data.logging_settings import configure_logger
from config_data.config import Config, TgBot
from database.dao.user_dao import UserAccessUserDAO
from utils.helpers import edit_message_media, calculate_weight_gain
from config_data.initial_settings import AppParams
# from database.db_client import Database
# from services.plot_service import create_plot
# from services.sensor import get_temp_hum
# from utils.helpers import edit_message_media, correct_temp_setting, correct_hum_setting
# from states.fsm import FSMSettingsForm


logger = configure_logger(__name__)
common_router = Router()


@common_router.message(CommandStart())
async def process_start_command(msg: Message,
                                bot_config: FromDishka[TgBot],
                                user_dao: FromDishka[UserAccessUserDAO],
                                weight_dao: FromDishka[UserAccessWeightsDAO],
                                ):
    logger.info(f"User {get_user_names(msg)} have start the bot")
    user = user_dao.get_one("telegram_id", msg.from_user.id)

    if user is None:
        reply_msg = (f"{create_hello_msg(msg)}\n"
                     f"Посмотрите инструкцию по использованию по кнопке help и вперёд.")
        user_dao.add_one({"username": get_user_names(msg), "telegram_id": msg.from_user.id})
    else:
        reply_msg = create_hello_msg(msg)
        # weight_dao.add_one({"user_id": msg.from_user.id, "weight": 100.5, "date_time": datetime.now(UTC)})
    await msg.bot.send_photo(chat_id=msg.from_user.id,
                             photo=random.choice(bot_config.bot_pic),
                             caption=reply_msg,
                             reply_markup=main_keyboard,
                             )


@common_router.callback_query(F.data == "backward_btn",)
async def process_back_click(callback: CallbackQuery,
                             bot: Bot,
                             bot_config: FromDishka[TgBot],
                             ):
    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             main_keyboard,
                             create_hello_msg(callback),
                             )


@common_router.callback_query(F.data == "track_btn",)
async def process_track_click(callback: CallbackQuery,
                              bot: Bot,
                              bot_config: FromDishka[TgBot],
                              weight_dao: FromDishka[UserAccessWeightsDAO],
                              ):
    weighins_count = weight_dao.get_count(callback.from_user.id)

    if weighins_count < AppParams.minimal_interval * 2:
        reply_text = create_not_enough_data_msg(weighins_count)
    else:
        last_week = weight_dao.get_awg_data(user_id=callback.from_user.id,
                                            page=0,
                                            limit=AppParams.minimal_interval,
                                            identifier_name="weight"
                                            )
        previous_week = weight_dao.get_awg_data(user_id=callback.from_user.id,
                                                page=1,
                                                limit=AppParams.minimal_interval,
                                                identifier_name="weight"
                                                )
        weight_gain = calculate_weight_gain(round(last_week, 2), round(previous_week, 2))
        reply_text = create_track_weight_msg(weight_gain)

    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             back_keyboard,
                             reply_text,
                             )


@common_router.message(Command(commands='help'))
async def process_help_command(msg: Message,
                               bot_config: FromDishka[TgBot],
                               ):
    await msg.bot.send_photo(chat_id=msg.from_user.id,
                             photo=random.choice(bot_config.bot_pic),
                             caption=help_msg,
                             reply_markup=back_keyboard,
                             )



# Этот хэндлер будет срабатывать на отправку боту фотоF.content_type == ContentType.PHOTO
@common_router.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    print(message.photo)
    print(message.photo[-1].file_id)
    await message.reply_photo(message.photo[-1].file_id)
