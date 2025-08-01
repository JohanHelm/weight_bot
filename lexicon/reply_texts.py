from aiogram.types import CallbackQuery, Message
from pandas.core.frame import DataFrame

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
            "Делайте взвешивания каждый день и заносите результаты "
            "в бот по кнопке ⚖️ ВЗВЕШИВАНИЕ.\n"
            "Результат можно вносить один раз в день.\n"
            "Для отслеживания тенденции изменения веса тела "
            "необходимо накопить массив данных взвешиваний за две недели.\n"
            "Данные по изменению веса можно получить по кнопке 👣 ТРЕКЕР ВЕСА.")


def create_not_enough_data_msg(weighins_count: int) -> str:
    return (f"Недостаточно данных измерений для оценки устойчивого изменения веса.\n"
            f"Продолжайте делать взвешивания еще "
            f"{AppParams.minimal_interval * 2 - weighins_count} дней.")


def create_track_weight_msg(weight_gain: float) -> str:
    if weight_gain == 0:
        msg = (f"Колебания веса вашего тела ниже {AppParams.threshold_percent}%.\n"
               f"У вас нет устойчивого набора или снижения веса.")
    elif weight_gain < 0:
        msg = f"За предидущую неделю вы похудели примерно на {weight_gain} кг."
    else:
        msg = f"За предидущую неделю вы набрали примерно {weight_gain} кг."
    return msg


def create_weighing_data_msg():
    return ("Введите ваш текущий вес в килограммах с точностью до второго знака после запятой.\n"
            "Допустимые значения от 1 до 300.\n"
            "(На вход принимаются целые числа и десятичные дроби.)")


def got_new_weighing_data_msg(weigh_data: float) -> str:
    return (f"Результат вашего взвешивания сегодня {weigh_data} кг.\n"
            f"Нажмите кнопку 👇 ПОДТВЕРДИТЬ чтобы сохранить этот результат.")


def create_confirmed_weighing_msg(weigh_data: float) -> str:
    return f"Результат вашего взвешивания сегодня {weigh_data} кг сохранён.\n"


def create_plot_title(two_weeks_df: DataFrame) -> str:
    return (f"Результаты взвешиваний с "
            f"{min(two_weeks_df.date.values)} по {max(two_weeks_df.date.values)}.")


bad_weighing_data_msg = "Введены некорректные данные!!!\n"

already_entered_weighing_data = "Cегодня вы уже внесли данные взвешивания"






