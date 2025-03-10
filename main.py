import logging
import asyncio
from aiogram import Bot, Dispatcher
from bot.config import config
from bot.handlers import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """Main bot class that handles initialization and startup"""
    
    def __init__(self, token: str):
        """Initialize bot with token
        
        Args:
            token (str): Telegram bot API token
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.setup_handlers()

    def setup_handlers(self):
        """Register all handlers"""
        self.dp.include_router(router)

    async def start(self):
        """Start the bot polling"""
        try:
            logger.info("Starting bot...")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

async def main():
    """Main function to start the bot"""
    bot = TelegramBot(token=config.bot.token)
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
