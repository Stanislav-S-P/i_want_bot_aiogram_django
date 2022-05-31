"""Файл для запуска бота. Содержит в себе все регистраторы приложения"""


from loader import dp
from aiogram.utils import executor
from handlers import start, contractors, clients, echo


start.register_handlers_start(dp)
clients.register_handlers_clients(dp)
contractors.register_handlers_contractors(dp)
echo.register_handlers_echo(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
