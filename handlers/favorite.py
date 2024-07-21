from aiogram import Router
from database.db_controller import db_controller
from aiogram.filters import Command


route = Router()


def favorite_db(user_id, film_id):
    db = db_controller
    db.toggle_favorite(user_id=user_id, film_id=film_id)


@route.message(Command("favorite"))
async def cmd_favorite():
    pass
