from aiogram import Router
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types


route = Router()


def history_db(user_id, film_id):
    db = db_controller
    db.add_history(user_id=user_id, film_id=film_id)


@route.message(Command("history"))
async def cmd_history(message: types.Message):
    await message.answer(f"datas = {db_controller.get_all_history()}")
