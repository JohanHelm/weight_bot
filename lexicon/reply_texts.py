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

def great_new_user(update: Message | CallbackQuery) -> str:
    return f"Привет новый пользователь {get_user_names(update)}"


