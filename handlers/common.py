import random

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, ContentType, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka

from config_data.config import TgBot
from config_data.initial_settings import AppParams
from config_data.logging_settings import configure_logger
from database.dao.user_dao import UserAccessUserDAO
from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (
    create_hello_msg,
    create_not_enough_data_msg,
    create_track_weight_msg,
    get_user_names,
    help_msg,
)
from markups.keyboards import back_keyboard, main_keyboard
from utils.helpers import calculate_weight_gain, edit_message_media


logger = configure_logger(__name__)
common_router = Router()


@common_router.message(CommandStart())
async def process_start_command(msg: Message,
                                bot_config: FromDishka[TgBot],
                                user_dao: FromDishka[UserAccessUserDAO],
                                ):
    logger.info(f"User {get_user_names(msg)} have start the bot")
    user = user_dao.get_one({"telegram_id": msg.from_user.id})
    if user is None:
        reply_msg = (f"{create_hello_msg(msg)}\n"
                     f"Посмотрите инструкцию по использованию по кнопке help и вперёд.")
        user_dao.add_one({"username": get_user_names(msg), "telegram_id": msg.from_user.id})
    else:
        reply_msg = create_hello_msg(msg)
    await msg.bot.send_photo(chat_id=msg.from_user.id,
                             photo=random.choice(bot_config.bot_pic),
                             caption=reply_msg,
                             reply_markup=main_keyboard,
                             )


@common_router.callback_query(F.data == "backward_btn",)
async def process_back_click(callback: CallbackQuery,
                             bot: Bot,
                             bot_config: FromDishka[TgBot],
                             state: FSMContext,
                             ):
    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             main_keyboard,
                             create_hello_msg(callback),
                             )
    await state.clear()


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
