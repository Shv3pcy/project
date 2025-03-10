import os
from dotenv import load_dotenv

# загрузка переменных среды
load_dotenv()

# получение переменных
BOT_TOKEN = os.getenv('BOT_TOKEN')
