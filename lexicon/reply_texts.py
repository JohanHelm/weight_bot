from aiogram.types import Message, CallbackQuery


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
            "Делайте взвешивания каждый день и заносите результаты в бот по кнопке ▶️ ВЗВЕСИТСЯ.\n"
            "Результат можно вносить один раз в день.\n"
            "Для отслеживания тенденции изменения веса тела необходимо накопить массив данных взвешиваний за две недели.")



