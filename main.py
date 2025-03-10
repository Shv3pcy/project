from aiogram import Bot, Dispatcher
import asyncio
from handlers import router
import config

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()  # обработчик команд
    dp.include_router(router)
    await dp.start_polling(bot)
    print("BOT ON (ВКЛ)")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("BOT OFF (ВЫКЛ)")
