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


async def parser(args: list) -> None:
    for item_id, title, url, url, price, sale_price in args:
        resp = requests.get(url=url, cookies=cookies).json()['recently'][0]

        try:
            new_price = resp['old_price']
            new_sale_price = resp['price']
        except KeyError:
            new_price = resp['price']
            new_sale_price = None
        result = f'{item_id}.{title}.{url}.{new_price}.{new_sale_price}'
        if new_sale_price != sale_price:
            db.update_item(item_id, new_price, new_sale_price)
            connection = await aio_pika.connect_robust(
                host='localhost'
            )
            async with connection:
                routing_key = 'parser'
                channel = connection.channel()
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=result.encode()
                    ),
                    routing_key=routing_key
                )
        else:
            print('Ok')
            continue


if __name__ == "__main__":
    while True:
        asyncio.run(parser(get_items()))
        time.sleep(30)

