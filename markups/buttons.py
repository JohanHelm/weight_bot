from aiogram.types import InlineKeyboardButton

backward_btn = InlineKeyboardButton(text="⏪ НАЗАД!", callback_data="backward_btn")

weighin_btn = InlineKeyboardButton(text="⚖️ ВЗВЕШИВАНИЕ.", callback_data="weighin_btn")

track_btn = InlineKeyboardButton(text="👣 ТРЕКЕР ВЕСА", callback_data="track_btn")

confirm_btn = InlineKeyboardButton(text="👇 ПОДТВЕРДИТЬ", callback_data="confirm_btn")

plot_btn = InlineKeyboardButton(text="📈 ГРАФИК", callback_data="0")

page_forward_btn = InlineKeyboardButton(text="➡️️", callback_data="-1")

page_backward_btn = InlineKeyboardButton(text="⬅️", callback_data="1")


def create_pages_total_btn(page: int, total_pages: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=f"{page} / {total_pages}️", callback_data="total_pages")
