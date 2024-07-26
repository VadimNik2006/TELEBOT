from aiogram import Router

from api.controller import api_controller
from database.db_controller import db_controller
from aiogram.filters import Command
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
# from keybords.cmd_favorite.favorite_inline import favorite_list_buttons
from utils import print_for_favorite_buttons


route = Router()


def favorite_db(user_id, film_id, add=True):
    db_controller.toggle_favorite(user_id=user_id, film_id=film_id, add=add)


@route.message(Command("favorite"))
async def cmd_favorite(message: types.Message, state: FSMContext):
    print("in fav_hand")
    # await message.answer(f"faves = {db_controller.get_all_faves()}")
    # await message.answer(text=f"<b>Избранные фильмы:</b> {favorite_list_buttons()}", parse_mode=ParseMode.HTML)
    await message.answer(
        text=f"<b>Избранные фильмы:</b> {print_for_favorite_buttons(favorite_data=db_controller.get_all_faves(), api_controller=api_controller)}",
        parse_mode=ParseMode.HTML)
    await state.set_state(state=None)
