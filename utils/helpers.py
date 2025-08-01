from math import fabs

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto
from pandas.core.frame import DataFrame
import pandas as pd

from config_data.initial_settings import AppParams
from database.models import Weights

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