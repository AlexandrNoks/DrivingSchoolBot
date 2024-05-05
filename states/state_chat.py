from aiogram.fsm.state import StatesGroup, State


class InfoChat(StatesGroup):
    user_id = State()
    user_name = State()
    user_phone = State()
    user_text = State()


class Schedule(StatesGroup):
    date_lesson = State()
    lesson = State()
    time = State()


class Students(StatesGroup):
    log_user = State()
    name_user = State()


class Remind(StatesGroup):
    new_lesson = State()
    new_ticher = State()
    del_lesson = State()


class PollChat(StatesGroup):
    user_name = State()
    user_id = State()
    user_text = State()


