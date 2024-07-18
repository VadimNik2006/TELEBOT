from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
import logging
from handlers import *


bot = Bot(token=config.bot_token.get_secret_value())
# logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(start_route, movie_search_route, help_route, favorite_route, history_route)
