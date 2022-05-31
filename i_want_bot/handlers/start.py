"""Файл содержащий обработчики команд"""


from aiogram import types, Dispatcher
from database.database import DataBaseModel
from keyboards.keyboards import start_menu_keyboards
from loader import bot, logger
from settings import constants
from keyboards import key_text
from .echo import custom_delete


async def start_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /start
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        if message.from_user.username is None:
            bot_message = await bot.send_message(
                message.from_user.id, constants.START_MESSAGE.format(
                    message.from_user.first_name
                ), reply_markup=start_menu_keyboards()
            )
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
        else:
            bot_message = await bot.send_message(
                message.from_user.id, constants.START_MESSAGE.format(
                    message.from_user.username
                ), reply_markup=start_menu_keyboards()
            )
            DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def help_handler(message: types.Message) -> None:
    """
    Хэндлер - обрабатывает команду /help
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        bot_message = await bot.send_message(message.from_user.id, constants.HELP_MESSAGE)
        DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_handlers_start(dp: Dispatcher):
    """Регистратор хэндлеров файла - Старт"""
    dp.register_message_handler(start_handler, commands=['start'], state=None)
    dp.register_message_handler(
        help_handler, lambda message: message.text.startswith((key_text.HELP, '/help')), state=None
    )
