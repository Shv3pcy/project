import logging
from aiogram import Bot, Dispatcher
import asyncio
from handlers import router
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()  # обработчик команд
        self.setup_handlers()

    def setup_handlers(self):
        self.dp.include_router(router)

    async def start(self):
        try:
            logger.info("Starting bot...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

async def main():
    bot = TelegramBot(token=config.BOT_TOKEN)
    await bot.start()
    logger.info("BOT ON (ВКЛ)")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("BOT OFF (ВЫКЛ)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
