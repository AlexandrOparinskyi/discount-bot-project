from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from database.database import ConnectDB
from lexicons.lexicon_ru import LEXICON_RU
from services.service import get_attributes
from keyboards.keyboards import create_confirm_keyboard

db = ConnectDB('database.db')


async def start_command(message: Message):
    user_id = message.from_user.id
    if not db.exists_user(user_id):
        db.add_user(user_id)
    await message.answer(LEXICON_RU[message.text])


async def help_command(message: Message):
    await message.answer(LEXICON_RU[message.text])


async def send_attributes(message: Message):

    title, image, url, api_url = get_attributes(message.text)
    await message.answer_photo(
        image,
        f"{title}\n\n{LEXICON_RU['item_question']}",
        reply_markup=create_confirm_keyboard()
    )


async def answer_yes(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(LEXICON_RU[callback.data].format(item='2345'))


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(send_attributes, lambda x: len(x.text) == 12)
    dp.register_callback_query_handler(answer_yes, text='yes')

