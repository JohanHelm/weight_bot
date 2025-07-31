import random
from _datetime import date

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka

from config_data.config import TgBot
from config_data.logging_settings import configure_logger
from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (
    already_entered_weighing_data,
    bad_weighing_data_msg,
    create_confirmed_weighing_msg,
    create_hello_msg,
    create_weighing_data_msg,
    got_new_weighing_data_msg,
)
from markups.keyboards import back_keyboard, confirm_keyboard, main_keyboard
from states.fsm import FSMWeighingForm
from utils.helpers import correct_weighing_data, edit_message_media

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
                            weight_dao: FromDishka[UserAccessWeightsDAO],
                            state: FSMContext):
    last_weigh_data = weight_dao.get_one({"user_id": callback.from_user.id, "date": str(date.today())})
    if last_weigh_data is None:
        await edit_message_media(callback,
                                 bot,
                                 random.choice(bot_config.bot_pic),
                                 back_keyboard,
                                 create_weighing_data_msg(),
                                 )
        await state.set_state(FSMWeighingForm.enter_weighing_data)
        await state.update_data(call=callback)
    else:
        await callback.answer(text=already_entered_weighing_data,
                              show_alert=True,
                              cache_time=3,
                              )


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
        await state.update_data(weigh_data=weigh_data)
        await edit_message_media(callback,
                                 bot,
                                 random.choice(bot_config.bot_pic),
                                 confirm_keyboard,
                                 got_new_weighing_data_msg(weigh_data),
                                 )
        await state.set_state(FSMWeighingForm.confirm_weighing_data)
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


@weighings_router.callback_query(F.data == "confirm_btn", StateFilter(FSMWeighingForm.confirm_weighing_data), )
async def confirm_weighing_data(callback: CallbackQuery,
                                bot: Bot,
                                bot_config: FromDishka[TgBot],
                                weight_dao: FromDishka[UserAccessWeightsDAO],
                                state: FSMContext,
                                ):
    state_data = await state.get_data()
    weigh_data = state_data.get("weigh_data")
    weight_dao.add_one({"user_id": callback.from_user.id, "weight": weigh_data, "date": date.today()})

    await callback.answer(text=create_confirmed_weighing_msg(weigh_data),
                          show_alert=True,
                          cache_time=3,
                          )
    await edit_message_media(callback,
                             bot,
                             random.choice(bot_config.bot_pic),
                             main_keyboard,
                             create_hello_msg(callback),
                             )
    await state.clear()
