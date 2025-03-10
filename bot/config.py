import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class BotConfig:
    """Bot configuration class"""
    token: str

@dataclass
class Config:
    """Main configuration class"""
    bot: BotConfig

# Create configuration instance
def load_config() -> Config:
    """Load configuration from environment variables"""
    return Config(
        bot=BotConfig(
            token=os.getenv('BOT_TOKEN')
        )
    )

# Export config instance
config = load_config()