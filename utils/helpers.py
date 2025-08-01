from math import fabs

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from pandas.core.frame import DataFrame
import pandas as pd

from config_data.initial_settings import AppParams
from database.models import Weights
from database.dao.weight_dao import UserAccessWeightsDAO

async def edit_message_media(callback: CallbackQuery,
                             bot: Bot,
                             media: str | BufferedInputFile,
                             markup: InlineKeyboardMarkup,
                             caption: str = ""):
    try:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=media, caption=caption),
            reply_markup=markup,
        )

    except TelegramBadRequest:
        await bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=InputMediaPhoto(media=media, caption=caption),
            reply_markup=markup
        )


def calculate_weight_gain(last_week: float, previous_week: float) -> float:
    natural_weight_fluctuations = round(max(last_week, previous_week) * AppParams.threshold_percent / 100, 2)
    weight_difference = round(last_week - previous_week, 2)

    if fabs(weight_difference) <= natural_weight_fluctuations:
        return 0
    else:
        return weight_difference


def correct_weighing_data(input_weight: str) -> bool:
    try:
        weigh_data = float(input_weight)
    except ValueError:
        return False
    else:
        return 1 <= weigh_data  <= 300


def models_2_df_converter(two_weeks: list[Weights]) -> DataFrame:
    return pd.DataFrame(
        {"date": (item.date for item in two_weeks),
         "weight": (item.weight for item in two_weeks),
         },
    )

async def get_plot_data(state: FSMContext,
                        callback: CallbackQuery,
                        weight_dao: UserAccessWeightsDAO,
                        weighins_count: int = 0,
                        ) -> tuple[list[Weights], int,int]:

    state_data = await state.get_data()
    page = state_data.get("page", 0) + int(callback.data)
    total_pages = state_data.get("total_pages", weighins_count // (AppParams.minimal_interval * 2))

    two_weeks = weight_dao.get_pack(user_id=callback.from_user.id,
                                    page=page,
                                    limit=AppParams.minimal_interval,
                                    )
    return two_weeks, page, total_pages
