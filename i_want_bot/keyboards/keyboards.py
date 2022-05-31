"""Файл - содержащий функции создания клавиатур"""


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import key_text


def start_menu_keyboards() -> ReplyKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру роли
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    first_key = KeyboardButton(key_text.CLIENT)
    second_key = KeyboardButton(key_text.CONTRACTOR)
    return keyboards.add(first_key, second_key)


def client_menu_keyboards() -> ReplyKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру действий роли заказчика
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    first_key = KeyboardButton(key_text.CREATE_TASK)
    second_key = KeyboardButton(key_text.MY_TASK)
    third_key = KeyboardButton(key_text.HELP)
    keyboards.add(first_key)
    keyboards.add(second_key, third_key)
    return keyboards


def contractor_menu_keyboards() -> ReplyKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру действий роли исполнителя
    :return: ReplyKeyboardMarkup
    """
    keyboards = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    first_key = KeyboardButton(key_text.TASK)
    second_key = KeyboardButton(key_text.MY_RESP)
    third_key = KeyboardButton(key_text.HELP)
    keyboards.add(first_key)
    keyboards.add(second_key, third_key)
    return keyboards


def delete_task_keyboards(task_id: int) -> InlineKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру к заданиям заказчика
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=1)
    key_show = InlineKeyboardButton(
        text=key_text.SHOW_RESP, callback_data=key_text.SHOW_RESP + ' ' + str(task_id)
    )
    key_delete = InlineKeyboardButton(
        text=key_text.DELETE_TASK, callback_data=key_text.DELETE_TASK + ' ' + str(task_id)
    )
    return keyboards.add(key_show, key_delete)


def resp_keyboards(task_id: int, clients_id: int) -> InlineKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру отклика к заданию
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=1)
    key = InlineKeyboardButton(
        text=key_text.RESP, callback_data=key_text.RESP + ' ' + str(task_id) + ' ' + str(clients_id)
    )
    return keyboards.add(key)


def task_limit(limit_task: int) -> InlineKeyboardMarkup:
    """
    Функция - создающая и возвращающая клавиатуру с кнопками переключения просмотра заданий
    :return: InlineKeyboardMarkup
    """
    keyboards = InlineKeyboardMarkup(row_width=2)
    page = limit_task // 10
    remains = limit_task % 10
    i_from = 1
    i_before = 10
    if page > 0:
        for _ in range(page):
            key_page = InlineKeyboardButton(
                text=key_text.TASK_KEY.format(i_from, i_before), callback_data=str(i_from) + ' ' + str(i_before)
            )
            keyboards.add(key_page)
            i_from += 10
            i_before += 10
    if remains > 0:
        i_before = i_before - 10 + remains
        key_page = InlineKeyboardButton(
            text=key_text.TASK_KEY.format(i_from, i_before), callback_data=str(i_from) + ' ' + str(i_before)
        )
        keyboards.add(key_page)
    return keyboards
