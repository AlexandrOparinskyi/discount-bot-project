from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from database.database import ConnectDB
from lexicons.lexicon_ru import LEXICON_RU
from services.get_attributes import Attributes
from keyboards.keyboards import create_confirm_keyboard

db = ConnectDB('database.db')
ARTICLE: str


def get_article(article: str) -> str:
    return article


async def start_command(message: Message):
    user_id = message.from_user.id
    if not db.exists_user(user_id):
        db.add_user(user_id)
    await message.answer(LEXICON_RU[message.text])


async def help_command(message: Message):
    await message.answer(LEXICON_RU[message.text])


async def send_attributes(message: Message):
    global ARTICLE
    ARTICLE = message.text.lstrip().rstrip()
    if not db.exists_item(message.text):
        attr = Attributes(message.text)
        title = attr.get_title()
        image = attr.get_image()
        price, sale_price = attr.get_prices()
        db.add_item(
            message.text,
            title,
            attr.get_url(),
            image,
            attr.get_api_url(),
            price,
            sale_price
        )
    else:
        title, image, price, sale_price = db.get_item(message.text)
    if sale_price is None:
        await message.answer_photo(
            image,
            f"{title}\n\n{LEXICON_RU['item_question']}",
            reply_markup=create_confirm_keyboard()
        )
    else:
        await message.answer(LEXICON_RU['item_with_sale'])


async def answer_yes(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id
    if not db.exists_users_item(user_id, ARTICLE):
        db.add_users_item(user_id, ARTICLE)
    await callback.message.answer(LEXICON_RU[callback.data])


async def answer_no(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(LEXICON_RU['no'])


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(send_attributes, lambda x: len(x.text) == 12)
    dp.register_callback_query_handler(answer_yes, text='yes')
    dp.register_callback_query_handler(answer_no, text='no')
