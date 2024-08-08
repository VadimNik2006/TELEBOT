from aiogram import Router
from aiogram.enums import ParseMode
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types
from utils import print_history
from api.controller import api_controller
from aiogram.fsm.context import FSMContext

route = Router()


def history_db(user_id, film_id):
    db_controller.add_history(user_id=user_id, film_id=film_id)


async def send_history(message: types.Message):
    data = print_history(history_data=db_controller.get_all_history(user_id=message.from_user.id),
                         api_controller=api_controller)
    await message.answer(
        text=f"<b>История запросов:</b> {data}",
        parse_mode=ParseMode.HTML)


@route.message(Command("history"))
async def cmd_history(message: types.Message, state: FSMContext):
    await send_history(message)
    await state.set_state(state=None)
