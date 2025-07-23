from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, BufferedInputFile, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest


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