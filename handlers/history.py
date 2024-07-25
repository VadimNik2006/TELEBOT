from aiogram import Router
from aiogram.enums import ParseMode
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types
from utils import print_history
from api.controller import api_controller
from pprint import pprint


route = Router()


def history_db(user_id, film_id):
    db = db_controller
    db.add_history(user_id=user_id, film_id=film_id)


@route.message(Command("history"))
async def cmd_history(message: types.Message):
    await message.answer(text=f"<b>История запросов:</b> {print_history(history_data=db_controller.get_all_history(), api_controller=api_controller)}", parse_mode=ParseMode.HTML)
