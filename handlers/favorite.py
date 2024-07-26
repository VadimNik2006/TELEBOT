from aiogram import Router
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types
from aiogram.fsm.context import FSMContext


route = Router()


def favorite_db(user_id, film_id):
    db = db_controller
    db.toggle_favorite(user_id=user_id, film_id=film_id)


@route.message(Command("favorite"))
async def cmd_favorite(message: types.Message, state: FSMContext):
    await message.answer(f"faves = {db_controller.get_all_faves()}")

    await state.set_state(state=None)


# @route.message(Command("history"))
# async def cmd_history(message: types.Message, state: FSMContext):
#     await message.answer(
#         text=f"<b>История запросов:</b> {print_history(history_data=db_controller.get_all_history(), api_controller=api_controller)}",
#         parse_mode=ParseMode.HTML)
#
#     await state.clear()