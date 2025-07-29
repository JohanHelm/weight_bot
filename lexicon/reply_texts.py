from aiogram.types import Message, CallbackQuery
from typing import Any

from config_data.initial_settings import AppParams


def get_user_names(update: Message | CallbackQuery) -> str:
    return " ".join(filter
                    (bool,
                     (update.from_user.first_name,
                      update.from_user.last_name,
                      update.from_user.username,
                      )
                     )
                    )


def create_hello_msg(update: Message | CallbackQuery) -> str:
    return f"Привет {get_user_names(update)}"

help_msg = ("Бот предназначен для контоля веса человеческого тела.\n"
            "Делайте взвешивания каждый день и заносите результаты в бот по кнопке ⚖️ ВЗВЕШИВАНИЕ.\n"
            "Результат можно вносить один раз в день.\n"
            "Для отслеживания тенденции изменения веса тела необходимо накопить массив данных взвешиваний за две недели.\n"
            "Данные по изменению веса можно получить по кнопке 👣 ТРЕКЕР ВЕСА.")


def create_not_enough_data_msg(weighins_count: int) -> str:
    return (f"Недостаточно данных измерений для оценки устойчивого изменения веса.\n"
            f"Продолжайте делать взвешивания еще {AppParams.minimal_interval * 2 - weighins_count} дней.")


def create_track_weight_msg(weight_gain: float) -> str:
    if weight_gain == 0:
        msg = (f"Колебания веса вашего тела ниже {AppParams.threshold_percent}%.\n"
               f"У вас нет устойчивого набора или снижения веса.")
    elif weight_gain < 0:
        msg = f"За предидущую неделю вы похудели примерно на {weight_gain} кг."
    else:
        msg = f"За предидущую неделю вы набрали примерно {weight_gain} кг."
    return msg



