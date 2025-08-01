from aiogram.types import InlineKeyboardMarkup

from markups.buttons import *

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[plot_btn],
                     [weighin_btn],
                     [track_btn],
                     ]
)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[backward_btn],
                     ]
)

confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[confirm_btn],
                     [backward_btn],
                     ]
)