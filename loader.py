from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
import logging
from handlers import h_route
# from keybords import kb_route


bot = Bot(token=config.bot_token.get_secret_value())
# logging.basicConfig(level=logging.INFO)
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(h_route)
