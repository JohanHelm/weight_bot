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

def page_keyboard(page:int, total_pages: int)->InlineKeyboardMarkup:
    if page == total_pages:
        first_row = [create_pages_total_btn(page, total_pages), page_forward_btn]
    elif page == 0:
        first_row = [page_backward_btn, create_pages_total_btn(page, total_pages)]
    else:
        first_row = [page_backward_btn, create_pages_total_btn(page, total_pages), page_forward_btn]

    return InlineKeyboardMarkup(
        inline_keyboard=[first_row,
                         [backward_btn],
                         ]
    )
