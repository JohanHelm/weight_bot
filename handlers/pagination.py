import random

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, ContentType, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import FromDishka

from config_data.config import TgBot
from config_data.initial_settings import AppParams, PlotParams
from config_data.logging_settings import configure_logger
from database.dao.user_dao import UserAccessUserDAO
from database.dao.weight_dao import UserAccessWeightsDAO
from lexicon.reply_texts import (
    create_hello_msg,
    create_not_enough_data_msg,
    create_track_weight_msg,
    get_user_names,
    help_msg,
    create_plot_title
)
from markups.keyboards import back_keyboard, main_keyboard
from utils.plot_service import create_plot
from utils.helpers import calculate_weight_gain, edit_message_media, models_2_df_converter


logger = configure_logger(__name__)
page_router = Router()



@page_router.callback_query(F.data == "plot_btn",)
async def process_plot_click(callback: CallbackQuery,
                             bot: Bot,
                             bot_config: FromDishka[TgBot],
                             weight_dao: FromDishka[UserAccessWeightsDAO],
                             ):
    weighins_count = weight_dao.get_count(callback.from_user.id)
    print(weighins_count)
    if weighins_count < AppParams.minimal_interval * 2:
        reply_text = create_not_enough_data_msg(weighins_count)
        media = random.choice(bot_config.bot_pic)
    else:

        two_weeks = weight_dao.get_pack(user_id=callback.from_user.id,
                                        page=0,
                                        limit=AppParams.minimal_interval,
                                        )
        two_weeks_df = models_2_df_converter(two_weeks)
        img_bytes = create_plot(two_weeks_df)
        media = BufferedInputFile(img_bytes.read(), filename=PlotParams.img_filename, )
        reply_text = create_plot_title(two_weeks_df)

    await edit_message_media(callback,
                             bot,
                             media,
                             back_keyboard,
                             reply_text,
                             )