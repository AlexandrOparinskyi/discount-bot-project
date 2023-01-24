from aiogram import Dispatcher
from aiogram.types import Message

from database.database import db
from lexicons.lexicon_ru import LEXICON_RU


async def start_command(message: Message):
    user_id = message.from_user.id
    if not db.exists_user(user_id):
        db.add_user(user_id)
    await message.answer(LEXICON_RU[message.text])


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
