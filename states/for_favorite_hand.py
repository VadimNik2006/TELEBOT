from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
route = Router()


class Keyword2(StatesGroup):
    add_to_fav = State()
    check_fav = State()
