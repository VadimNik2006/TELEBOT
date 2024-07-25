from aiogram import Router
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types


route = Router()


def favorite_db(user_id, film_id):
    db = db_controller
    db.toggle_favorite(user_id=user_id, film_id=film_id)


@route.message(Command("favorite"))
async def cmd_favorite(message: types.Message):
    await message.answer(f"faves = {db_controller.get_all_faves()}")
