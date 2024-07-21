from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
route = Router()


class Keyword(StatesGroup):
    wait_from_similar = State()
    wait_film = State()
