"""Сценарий исполнителя"""


import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from database.models import FSMResp, FSMPhone
from handlers.echo import custom_delete
from handlers.start import start_handler, help_handler
from keyboards import key_text
from database.database import DataBaseModel
from keyboards.keyboards import resp_keyboards, contractor_menu_keyboards, task_limit
from loader import bot, dp, logger
from settings import constants


async def role_contractor_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает текст роли исполнителя
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        if not DataBaseModel.select_check_user(message.from_user.id, message.text):
            if message.from_user.username is None:
                await FSMPhone.phone.set()
                bot_message = await bot.send_message(message.from_user.id, constants.PHONE_WARNING)
                DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
                bot_message = await bot.send_message(message.from_user.id, constants.PHONE_INPUT)
                DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            else:
                DataBaseModel.insert_user((message.from_user.id, message.from_user.username, message.text))
                await bot.send_message(
                    message.from_user.id, constants.ACTION_MESSAGE, reply_markup=contractor_menu_keyboards()
                )
        else:
            await bot.send_message(
                message.from_user.id, constants.ACTION_MESSAGE, reply_markup=contractor_menu_keyboards()
            )
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def phone_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает введенный номер телефона пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        if message.text.startswith('+7') and [message.text[2:]] == re.findall(pattern, message.text[2:]) \
                and len(message.text) >= 12:
            DataBaseModel.insert_user((message.from_user.id, message.text, key_text.CONTRACTOR))
            await state.finish()
            bot_message = await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            await bot.send_message(
                message.from_user.id, constants.ACTION_MESSAGE, reply_markup=contractor_menu_keyboards()
            )
        elif message.text.startswith('8') and [message.text[1:]] == re.findall(pattern, message.text[1:]) \
                and len(message.text) >= 11:
            DataBaseModel.insert_user((message.from_user.id, message.text, key_text.CONTRACTOR))
            await state.finish()
            bot_message = await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            await bot.send_message(
                message.from_user.id, constants.ACTION_MESSAGE, reply_markup=contractor_menu_keyboards()
            )
        elif [message.text] == re.findall(pattern, message.text) and len(message.text) >= 10:
            DataBaseModel.insert_user((message.from_user.id, message.text, key_text.CONTRACTOR))
            await state.finish()
            bot_message = await bot.send_message(message.from_user.id, constants.PHONE_COMPLETE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            await bot.send_message(
                message.from_user.id, constants.ACTION_MESSAGE, reply_markup=contractor_menu_keyboards()
            )
        else:
            bot_message = await bot.send_message(message.from_user.id, constants.INCORRECT_PHONE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            bot_message = await bot.send_message(message.from_user.id, constants.PHONE_INPUT)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


"""Просмотр заданий"""


async def contractors_task(message: types.Message) -> None:
    """
    Хэндлер - Проверяет данные в БД. В случае наличия данных, отправляет пользователю кнопки выбора заданий.
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        tasks = DataBaseModel.select_all_task()
        if tasks:
            limit_task = len(tasks)
            bot_message = await bot.send_message(
                message.from_user.id, constants.CHOICES_TASKS.format(limit_task), reply_markup=task_limit(limit_task)
            )
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        else:
            bot_message = await bot.send_message(message.from_user.id, constants.EMPTY_TASKS)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def choice_task_handler(call: types.CallbackQuery) -> None:
    """
    Хэндлер - Проверяет данные в БД. Отправляет пользователю список
    заданий с кнопками отклика.
    :param call: CallbackQuery
    :return: None
    """
    try:
        await custom_delete(call.message.chat.id)
        await FSMResp.task_user.set()
        call_data = call.data.split()
        limit = int(call_data[1]) - int(call_data[0]) + 1
        tasks = DataBaseModel.select_limit_task(int(call_data[0]) - 1, limit)
        for elem in tasks:
            bot_message = await bot.send_message(
                call.from_user.id,
                constants.TASK_TEMPLATE_CONTRACTORS.format(elem[2], elem[3]),
                reply_markup=resp_keyboards(elem[0], elem[1]),
                parse_mode='Markdown'
            )
            DataBaseModel.insert_bot_message(call.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def callback_response(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хэндлер - Реагирует на нажатие кнопки Откликнуться.
    :param state: FSMContext
    :param call: CallbackQuery
    :return: None
    """
    try:
        await custom_delete(call.message.chat.id)
        async with state.proxy() as data:
            call_data = call.data.split()
            data['task_user'] = [call_data[2], call_data[3]]
        await FSMResp.next()
        bot_message = await bot.send_message(call.from_user.id, constants.RESP_MESSAGE)
        DataBaseModel.insert_bot_message(call.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def response_message(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - обрабатывает введённый пользователем отклик на задание
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        async with state.proxy() as data:
            username = DataBaseModel.select_resp_username(message.from_user.id)
            flag = True
            for sym in username[0]:
                if sym.isalpha():
                    flag = False
                    break
            if flag is False:
                username = '@' + username[0]
                DataBaseModel.insert_task_resp((
                    message.from_user.id, username, data['task_user'][0], message.text
                ))
            else:
                DataBaseModel.insert_task_resp((
                    message.from_user.id, username[0], data['task_user'][0], message.text
                ))
            bot_message = await bot.send_message(
                data['task_user'][1], constants.NEW_RESP_MESSAGE.format(username, message.text), parse_mode='Markdown'
            )
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        await state.finish()
        bot_message = await bot.send_message(message.from_user.id, constants.RESP_COMPLETE)
        DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


"""Просмотр своих откликов"""


async def contractors_resp(message: types.Message):
    """
    Хэндлер - Проверяет данные в БД. В случае наличия данных,
    выводит список заданий с откликами, на которые откликнулся пользователь.
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        tasks = DataBaseModel.select_task_id_resp(message.from_user.id)
        if tasks:
            for elem in tasks:
                task = DataBaseModel.select_task_my_resp(elem[3])
                if task:
                    bot_message = await bot.send_message(
                        message.from_user.id,
                        constants.MY_RESP_TEMPLATE.format(task[0], task[1], elem[4]),
                        parse_mode='Markdown'
                    )
                    DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        else:
            bot_message = await bot.send_message(message.from_user.id, constants.EMPTY_MY_RESP)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


@dp.message_handler(Text(equals='/start'), state='*')
@dp.message_handler(Text(equals='/help'), state='*')
@dp.message_handler(Text(equals=key_text.HELP), state='*')
@dp.message_handler(Text(equals=key_text.MY_RESP), state='*')
@dp.message_handler(Text(equals=key_text.TASK), state='*')
async def cancel_contractors(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - реагирует на команды и выводит из машины состояния пользователя
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    if message.text == '/start':
        await start_handler(message)
    elif message.text == '/help' or message.text.startswith(key_text.HELP):
        await help_handler(message)
    elif message.text .startswith(key_text.MY_RESP):
        await contractors_resp(message)
    elif message.text.startswith(key_text.TASK):
        await contractors_task(message)


def register_handlers_contractors(dp: Dispatcher):
    """Регистратор хэндлеров файла - исполнители"""
    dp.register_message_handler(
        role_contractor_handler, lambda message: key_text.CONTRACTOR in message.text, state=None
    )
    dp.register_message_handler(contractors_task, lambda message: message.text.startswith(key_text.TASK), state=None)
    dp.register_callback_query_handler(
        callback_response, lambda call: call.data.startswith(key_text.RESP), state=FSMResp.task_user
    )
    dp.register_message_handler(response_message, content_types=['text'], state=FSMResp.resp_text)
    dp.register_message_handler(contractors_resp, lambda message: message.text.startswith(key_text.MY_RESP), state=None)
    dp.register_message_handler(phone_handler, content_types=['text'], state=FSMPhone.phone)
    dp.register_callback_query_handler(
        choice_task_handler, lambda call: call.data.startswith(
            ('1', '2,' '3', '4', '5', '6', '7', '8', '9')
        ), state=None
    )
