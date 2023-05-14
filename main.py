import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import service_handlers, action_handlers, dialog_handlers


load_dotenv()

bot = Bot(token=os.getenv('API_TOKEN'))

dp = Dispatcher()
dp.include_routers(service_handlers.router, action_handlers.router, dialog_handlers.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
