from math import fabs
from typing import Any
from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, BufferedInputFile, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

from config_data.initial_settings import AppParams


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

