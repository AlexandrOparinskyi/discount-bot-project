import asyncio
import logging
from typing import NoReturn
from asyncio import exceptions as async_ex

from aiogram import Bot, Dispatcher
from aiogram import exceptions as aio_ex

from config_data.config import load_config
from handlers.user_handlers import register_user_handlers

logging.basicConfig(
    filename='debug.txt',
    filemode='a',
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(asctime)s | %(message)s"
)


def register_all_handlers(dp: Dispatcher) -> NoReturn:
    register_user_handlers(dp)


async def main() -> NoReturn:
    bot: Bot = load_config()
    dp: Dispatcher = Dispatcher(bot)

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    except aio_ex:
        logging.error(aio_ex)
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except async_ex:
        logging.error(async_ex)
