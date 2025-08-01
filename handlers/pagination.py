import random

from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import BufferedInputFile, CallbackQuery
from dishka.integrations.aiogram import FromDishka

from config_data.config import TgBot
from config_data.initial_settings import AppParams, PlotParams
from config_data.logging_settings import configure_logger
from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (
    create_not_enough_data_msg,
    create_plot_title,
)
from markups.keyboards import back_keyboard, page_keyboard
from states.fsm import FSMPageForm
from utils.helpers import edit_message_media, get_plot_data, models_2_df_converter
from utils.plot_service import create_plot

logger = configure_logger(__name__)
page_router = Router()


@page_router.callback_query(F.data == "0", StateFilter(default_state))
async def process_plot_click(callback: CallbackQuery,
                             bot: Bot,
                             bot_config: FromDishka[TgBot],
                             weight_dao: FromDishka[UserAccessWeightsDAO],
                             state: FSMContext,
                             ):
    weighins_count = weight_dao.get_count(callback.from_user.id)
    if weighins_count < AppParams.minimal_interval * 2:
        reply_text = create_not_enough_data_msg(weighins_count)
        media = random.choice(bot_config.bot_pic)
        reply_keyboard = back_keyboard
    else:
        two_weeks, page, total_pages = await get_plot_data(state,
                                                           callback,
                                                           weight_dao,
                                                           weighins_count)
        two_weeks_df = models_2_df_converter(two_weeks)
        img_bytes = create_plot(two_weeks_df)
        media = BufferedInputFile(img_bytes.read(), filename=PlotParams.img_filename, )
        reply_text = create_plot_title(two_weeks_df)
        reply_keyboard = page_keyboard(page, total_pages)
        await state.set_state(FSMPageForm.set_page)
        await state.update_data(page=page,
                                total_pages=total_pages,
                                )

    await edit_message_media(callback,
                             bot,
                             media,
                             reply_keyboard,
                             reply_text,
                             )


@page_router.callback_query(F.data == "1", StateFilter(FSMPageForm.set_page))
async def process_backward_page(callback: CallbackQuery,
                                bot: Bot,
                                weight_dao: FromDishka[UserAccessWeightsDAO],
                                state: FSMContext,
                                ):
    two_weeks, page, total_pages = await get_plot_data(state, callback, weight_dao)
    two_weeks_df = models_2_df_converter(two_weeks)
    img_bytes = create_plot(two_weeks_df)
    media = BufferedInputFile(img_bytes.read(), filename=PlotParams.img_filename, )
    reply_text = create_plot_title(two_weeks_df)
    await state.update_data(page=page,
                            total_pages=total_pages,
                            )

    await edit_message_media(callback,
                             bot,
                             media,
                             page_keyboard(page, total_pages),
                             reply_text,
                             )


@page_router.callback_query(F.data == "-1", StateFilter(FSMPageForm.set_page))
async def process_forward_page(callback: CallbackQuery,
                                bot: Bot,
                                weight_dao: FromDishka[UserAccessWeightsDAO],
                                state: FSMContext,
                                ):
    two_weeks, page, total_pages = await get_plot_data(state, callback, weight_dao)
    two_weeks_df = models_2_df_converter(two_weeks)
    img_bytes = create_plot(two_weeks_df)
    media = BufferedInputFile(img_bytes.read(), filename=PlotParams.img_filename, )
    reply_text = create_plot_title(two_weeks_df)
    await state.update_data(page=page,
                            total_pages=total_pages,
                            )

    await edit_message_media(callback,
                             bot,
                             media,
                             page_keyboard(page, total_pages),
                             reply_text,
                             )
