import asyncio
import os
import time

import aio_pika
import requests
from dotenv import load_dotenv

from database.database import ConnectDB

load_dotenv()

db = ConnectDB('../database.db')

cookies = {
    'Cookie': os.getenv('COOKIE')
}


def get_items() -> list:
    return db.get_items_urls()


async def send(message: str) -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        routing_key = "parser"

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode(),
            ),
            routing_key=routing_key,
        )


async def parser(args: list) -> None:
    for ID, item_id, title, url, price, sale_price in args:
        resp = requests.get(url=url, cookies=cookies).json()['recently'][0]
        try:
            new_price = resp['old_price']
            new_sale_price = resp['price']
        except KeyError:
            new_price = resp['price']
            new_sale_price = None
        result = f'{ID}.{item_id}.{title}.{url}.{new_price}.{new_sale_price}'
        if new_sale_price != sale_price:
            db.update_item(item_id, new_price, new_sale_price)
            await send(result)
            print('Ready')
            await asyncio.sleep(5)
        else:
            print('Ok')
            await asyncio.sleep(5)
            continue


if __name__ == "__main__":
    while True:
        asyncio.run(parser(get_items()))


