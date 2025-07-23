from aiogram.types import InlineKeyboardMarkup

from markups.buttons import *


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[weighin_btn], [track_btn]]
)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[backward_btn],]
)