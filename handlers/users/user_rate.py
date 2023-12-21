from aiogram import types

from loader import dp
from utils.db_api.api import get_news, add_user_keywords, get_all_users


@dp.callback_query_handler()
async def rate(query: types.CallbackQuery):
    type = query.data.split(':')[0]
    if type == 'like':
        id = query.data.split(':')[1]
        news = get_news(id=id)
        print(news, id)
        add_user_keywords(id=query.from_user.id, new_keywords=news[1])
    await query.message.edit_reply_markup(reply_markup=None)

    print(get_all_users())
