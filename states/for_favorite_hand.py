from aiogram import Router
from aiogram.fsm.state import StatesGroup, State


route = Router()


class FavoriteStates(StatesGroup):
    wait_number = State()
