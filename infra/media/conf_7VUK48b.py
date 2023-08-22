import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

load_dotenv()

# main settings
API_URL = f'http://{os.getenv("API_HOST")}:{os.getenv("API_PORT")}/api/'
TOKEN = os.getenv('TOKEN')


# storage
storage = MemoryStorage()


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
