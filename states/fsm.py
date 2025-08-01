from aiogram.fsm.state import State, StatesGroup


class FSMWeighingForm(StatesGroup):
    enter_weighing_data = State()
    confirm_weighing_data = State()


class FSMPageForm(StatesGroup):
    set_page = State()
