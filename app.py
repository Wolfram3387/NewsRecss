import asyncio
from aiojobs.aiohttp import setup, spawn
from handlers.users.check_news import check_news
from utils.db_api.api import get_news_id
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


async def periodic_function():
    while True:
        await asyncio.sleep(30)
        await check_news()
        # print(*get_news_id(),sep='\n')


async def main():
    scheduler = await setup()
    await spawn(scheduler, periodic_function())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_function())
    executor.start_polling(dp, on_startup=on_startup)
