import asyncio
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, ContentType, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext


# from filters.my_filters import LabEmployee
from lexicon.reply_texts import (create_hello_msg,
                                 get_user_names,
                                 create_current_alarm_settings_msg,
                                 set_new_setting_msg,
                                 new_temp_setting_set,
                                 new_hum_setting_set,
                                 bad_new_setting_msg,
                                 acknowledge_msg,
                                 )
# from keyboards.markups import main_markup, back_markup, set_params_markup
from config_data.logging_settings import configure_logger
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
                bot_pic: str,
                ):
    logger.info(f"User {get_user_names(msg)} have start the bot")
    await msg.bot.send_photo(chat_id=msg.from_user.id,
                             photo=bot_pic,
                             caption=create_hello_msg(msg),
                             # reply_markup=main_markup,
                             )





# Этот хэндлер будет срабатывать на отправку боту фотоF.content_type == ContentType.PHOTO
@main_router.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    print(message.photo)
    print(message.photo[-1].file_id)
    await message.reply_photo(message.photo[-1].file_id)
