import random
from _datetime import datetime, UTC
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, ContentType, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from dishka.integrations.aiogram import FromDishka

from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (create_weighing_data_msg,
                                 create_hello_msg,
                                 bad_weighing_data_msg,
                                 got_new_weighing_data_msg,
                                 create_track_weight_msg,
                                 create_not_enough_data_msg,
                                 )

from markups.keyboards import main_keyboard, back_keyboard, confirm_keyboard
from config_data.logging_settings import configure_logger
from config_data.config import Config, TgBot
from database.dao.user_dao import UserAccessUserDAO
from utils.helpers import edit_message_media, correct_weighing_data
from config_data.initial_settings import AppParams
# from database.db_client import Database
# from services.plot_service import create_plot
# from services.sensor import get_temp_hum
# from utils.helpers import edit_message_media, correct_temp_setting, correct_hum_setting
from states.fsm import FSMWeighingForm




logger = configure_logger(__name__)
weighings_router = Router()


@weighings_router.callback_query(F.data == "backward_btn", ~StateFilter(default_state))
async def process_cancel_command_state(callback: CallbackQuery,
                                       bot: Bot,
                                       bot_config: FromDishka[TgBot],
                                       state: FSMContext):
    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             main_keyboard,
                             create_hello_msg(callback),
                             )
    await state.clear()


@weighings_router.callback_query(F.data == "weighin_btn", StateFilter(default_state))
async def set_weighing_data(callback: CallbackQuery,
                            bot: Bot,
                            bot_config: FromDishka[TgBot],
                            state: FSMContext):
    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             back_keyboard,
                             create_weighing_data_msg(),
                             )
    await state.set_state(FSMWeighingForm.enter_weighing_data)
    await state.update_data(call=callback)


@weighings_router.message(StateFilter(FSMWeighingForm.enter_weighing_data), )
async def process_weighing_data(msg: Message,
                               bot: Bot,
                               bot_config: FromDishka[TgBot],
                               state: FSMContext,
                               ):
    if correct_weighing_data(msg.text):
        await msg.delete()
        state_data = await state.get_data()
        callback = state_data.get("call")
        weigh_data = round(float(msg.text), 2)
        # db_instance.set_alarm_setting("temp", new_temp_setting)
        await state.clear()
        await edit_message_media(callback,
                                 bot,
                                 random.choice(bot_config.bot_pic),
                                 confirm_keyboard,
                                 got_new_weighing_data_msg(weigh_data),
                                 )
    else:
        await msg.delete()
        state_data = await state.get_data()
        callback = state_data.get("call")
        await edit_message_media(callback,
                                 bot,
                                 random.choice(bot_config.bot_pic),
                                 back_keyboard,
                                 f"{bad_weighing_data_msg}{create_weighing_data_msg()}",
                                 )