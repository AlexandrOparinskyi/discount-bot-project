import asyncio
import os

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


async def send(message: str, users: list[tuple[int]]) -> None:
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )

    async with connection:
        routing_key = "parser"

        channel = await connection.channel()

        for user in users:
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    app_id=f'{user[0]}'
                ),
                routing_key=routing_key,
            )


async def parser(args: list) -> None:
    for item_id, title, url, api_url, price, sale_price in args:
        resp = requests.get(url=api_url, cookies=cookies).json()['recently'][0]
        try:
            new_price = resp['old_price']
            new_sale_price = resp['price']
        except KeyError:
            new_price = resp['price']
            new_sale_price = None
        result = f"Теперь цена на {title} {new_sale_price}👍 вместо {new_price}👎\n\n" \
                 f"Скорее жми на смайлики <a href='{url}'>💰🤑✔ </a>"
        if new_sale_price != sale_price:
            users_id = db.get_users_item(item_id)
            db.update_item(item_id, new_price, new_sale_price)
            await send(result, users_id)
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(5)
            continue


if __name__ == "__main__":
    while True:
        asyncio.run(parser(get_items()))


