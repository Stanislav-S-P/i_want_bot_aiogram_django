"""Сценарий заказчика"""


from aiogram.dispatcher.filters import Text
from handlers.echo import custom_delete
from handlers.start import start_handler, help_handler
from keyboards import key_text
from keyboards.keyboards import delete_task_keyboards, client_menu_keyboards
from loader import bot, dp, logger
from settings import constants
from database.models import FSMTask
from database.database import DataBaseModel
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def role_client_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает текст роли заказчика
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        if not DataBaseModel.select_check_user(message.from_user.id, message.text):
            if message.from_user.username is None:
                DataBaseModel.insert_user((message.from_user.id, message.from_user.first_name, message.text))
            else:
                DataBaseModel.insert_user((message.from_user.id, message.from_user.username, message.text))
        await bot.send_message(
            message.from_user.id, constants.ACTION_MESSAGE, reply_markup=client_menu_keyboards()
        )
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


"""Создание задания"""


async def create_task(message: types.Message) -> None:
    """
    Хэндлер - входит в состояние создания задания. Просит пользователя ввести описание.
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        await FSMTask.title.set()
        bot_message = await bot.send_message(message.from_user.id, constants.TITLE_MESSAGE)
        DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def title_message(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - продолжает работать в состоянии создания задания. Просит пользователя ввести цену.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        async with state.proxy() as data:
            data['title'] = message.text
        await FSMTask.next()
        bot_message = await bot.send_message(message.from_user.id, constants.PRICE_MESSAGE)
        DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def price_message(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер - В случае корректно введённой стоимости, завершает создание задания.
    В случае не корректного ввода, просит ввести стоимость снова.
    :param message: Message
    :param state: FSMContext
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        if message.text.isdigit():
            async with state.proxy() as data:
                DataBaseModel.insert_task((message.from_user.id, data['title'], message.text, 'Другое', 'Активный'))
            await state.finish()
            bot_message = await bot.send_message(message.from_user.id, constants.TASK_COMPLETE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        else:
            bot_message = await bot.send_message(message.from_user.id, constants.INCORRECT_PRICE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
            bot_message = await bot.send_message(message.from_user.id, constants.PRICE_MESSAGE)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


"""Просмотр и удаление заданий"""


async def my_task(message: types.Message) -> None:
    """
    Хэндлер - Проверяет данные в БД. В случае наличия данных, отправляет пользователю список
    его созданных заданий. В противном случае, выводит сообщение о том, что задания ещё не созданы.
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        my_tasks = DataBaseModel.select_my_task(message.from_user.id)
        if my_tasks:
            for elem in my_tasks:
                count_resp = DataBaseModel.select_count_task_resp(elem[0])
                bot_message = await bot.send_message(
                    message.from_user.id,
                    constants.TASK_TEMPLATE.format(elem[1], elem[2], count_resp[0]),
                    reply_markup=delete_task_keyboards(elem[0]),
                    parse_mode='Markdown'
                )
                DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        else:
            bot_message = await bot.send_message(message.from_user.id, constants.EMPTY_TASK)
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def callback_task(call: types.CallbackQuery) -> None:
    """
    Хэндлер - Реагирует на нажатие кнопок (просмотреть отклики, удалить), далее действует по сценарию.
    :param call: CallbackQuery
    :return: None
    """
    try:
        await custom_delete(call.message.chat.id)
        if call.data.startswith(key_text.SHOW_RESP):
            call_data = call.data.split()
            resp = DataBaseModel.select_task_resp(int(call_data[3]))
            if resp:
                for elem in resp:
                    bot_message = await bot.send_message(
                        call.from_user.id, constants.RESP_TEMPLATE.format(elem[0], elem[1])
                    )
                    DataBaseModel.insert_bot_message(call.from_user.id, bot_message.message_id)
            else:
                bot_message = await bot.send_message(call.from_user.id, constants.EMPTY_RESP)
                DataBaseModel.insert_bot_message(call.from_user.id, bot_message.message_id)
        else:
            call_data = call.data.split()
            DataBaseModel.delete_task(int(call_data[3]))
            DataBaseModel.delete_task_resp(int(call_data[3]))
            bot_message = await bot.send_message(call.from_user.id, constants.TASK_DELETE)
            DataBaseModel.insert_bot_message(call.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


@dp.message_handler(Text(equals='/start'), state='*')
@dp.message_handler(Text(equals='/help'), state='*')
@dp.message_handler(Text(equals=key_text.HELP), state='*')
@dp.message_handler(Text(equals=key_text.CREATE_TASK), state='*')
@dp.message_handler(Text(equals=key_text.MY_TASK), state='*')
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
    elif message.text.startswith(key_text.CREATE_TASK):
        await create_task(message)
    elif message.text.startswith(key_text.MY_TASK):
        await my_task(message)


def register_handlers_clients(dp: Dispatcher):
    """Регистратор хэндлеров файла - Заказчик"""
    dp.register_message_handler(role_client_handler, lambda message: key_text.CLIENT in message.text, state=None)
    dp.register_message_handler(create_task, lambda message: message.text.startswith(key_text.CREATE_TASK), state=None)
    dp.register_message_handler(title_message, content_types=['text'], state=FSMTask.title)
    dp.register_message_handler(price_message, content_types=['text'], state=FSMTask.price)
    dp.register_message_handler(my_task, lambda message: message.text.startswith(key_text.MY_TASK), state=None)
    dp.register_callback_query_handler(callback_task, lambda call: call.data.startswith(
        (key_text.DELETE_TASK, key_text.SHOW_RESP)
    ), state=None)
