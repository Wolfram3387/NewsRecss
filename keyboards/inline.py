from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_markup(news_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='👍', callback_data=f'like:{news_id}'),
            InlineKeyboardButton(text='👎', callback_data='dislike')
        ]
    ])
