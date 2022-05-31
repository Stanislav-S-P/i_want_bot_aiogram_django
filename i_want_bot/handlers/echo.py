"""Файл содержащий Эхо-хэндлер и кастомную функцию подчистки сообщений"""


from aiogram import types, Dispatcher
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted

from database.database import DataBaseModel
from loader import bot, logger
from settings import constants


async def custom_delete(user_id: int) -> None:
    """
    Функция для подчистки сообщений бота
    :param user_id: int
    :return: None
    """
    try:
        result = DataBaseModel.select_bot_message(user_id)
        if result:
            if len(result) == 1:
                try:
                    await bot.delete_message(result[0][1], result[0][2])
                except MessageToDeleteNotFound:
                    pass
                except MessageCantBeDeleted:
                    DataBaseModel.delete_bot_message(user_id)
            else:
                for elem in result:
                    try:
                        await bot.delete_message(elem[1], elem[2])
                    except MessageToDeleteNotFound:
                        pass
                    except MessageCantBeDeleted:
                        DataBaseModel.delete_bot_message(user_id)
        DataBaseModel.delete_bot_message(user_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


async def echo_handler(message: types.Message):
    """
    Хэндлер - оповещает бота о некорректной команде (Эхо)
    :param message: Message
    :return: None
    """
    try:
        await custom_delete(message.chat.id)
        await message.delete()
        bot_message = await bot.send_message(message.from_user.id, constants.EMPTY_COMMAND)
        DataBaseModel.insert_bot_message(message.from_user.id, bot_message.message_id)
    except Exception as error:
        logger.error('В работе бота возникло исключение', exc_info=error)


def register_handlers_echo(dp: Dispatcher):
    """Регистратор хэндлеров файла - Эхо"""
    dp.register_message_handler(echo_handler)
