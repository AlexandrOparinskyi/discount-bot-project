import os
from typing import NoReturn

from aiogram import Bot
from dotenv import load_dotenv
import logging

load_dotenv()


class Connect:

    def __init__(self, token) -> NoReturn:
        self.token = token

    def bot(self) -> Bot:
        bot = Bot(
            token=self.token,
            parse_mode='HTML'
        )
        return bot


def load_config() -> Bot:
    c = Connect(os.getenv('TOKEN'))
    return c.bot()
