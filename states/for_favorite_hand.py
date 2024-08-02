from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
route = Router()


class FavoriteStates(StatesGroup):
    next = State()
    prev = State()
