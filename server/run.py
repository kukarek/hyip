import logging
from aiogram import Bot, Dispatcher, executor
from misc.config import API_TOKEN
from handlers import register_all_handlers

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)
    

def main() -> None:

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)


if __name__ == "__main__":
    main()