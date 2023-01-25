import asyncio
import aio_pika
import logging
from typing import NoReturn
from asyncio import exceptions as async_ex

from aiogram import Bot, Dispatcher
from aiogram import exceptions as aio_ex

from config_data.config import load_config
from handlers.user_handlers import register_user_handlers
from database.database import ConnectDB

logging.basicConfig(
    filename='debug.txt',
    filemode='a',
    level=logging.INFO,
    format=f"%(levelname)s | %(name)s | %(asctime)s | %(message)s"
)

db = ConnectDB('database.db')

bot: Bot = load_config()


def register_all_handlers(dp: Dispatcher) -> NoReturn:
    register_user_handlers(dp)


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        await bot.send_message(424306502, message.body)
        await asyncio.sleep(1)


async def rabbit():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    queue_name = "parser"
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=100)

    queue = await channel.declare_queue(queue_name)

    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


async def connect_bot() -> NoReturn:
    dp: Dispatcher = Dispatcher(bot)

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    except aio_ex:
        logging.error(aio_ex)
        await bot.close()


async def main() -> NoReturn:
    await asyncio.gather(
        connect_bot(),
        rabbit()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except async_ex:
        logging.error(async_ex)
