from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)


def create_confirm_keyboard() -> InlineKeyboardMarkup:
    confirm_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    confirm_keyboard.add(
        InlineKeyboardButton(
            text='Да',
            callback_data='yes'
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data='no'
        )
    )
    return confirm_keyboard


