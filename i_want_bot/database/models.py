from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMTask(StatesGroup):
    title = State()
    price = State()


class FSMResp(StatesGroup):
    task_user = State()
    resp_text = State()


class FSMPhone(StatesGroup):
    phone = State()
