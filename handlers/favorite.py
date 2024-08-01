from aiogram import Router

from api.controller import api_controller
from database.db_controller import db_controller
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from keybords.cmd_favorite.favorite_inline import *
from utils import print_for_favorite_buttons

# from keybords.cmd_favorite.favorite_inline import favorite_list_buttons


route = Router()


def favorite_db(user_id, film_id, add=True):
    db_controller.toggle_favorite(user_id=user_id, film_id=film_id, add=add)


async def send_favorite(message: types.Message):
    favorite_data = db_controller.get_all_faves(user_id=message.from_user.id)
    await message.answer(
        text=f"<b>Избранные фильмы:</b> {print_for_favorite_buttons(favorite_data=favorite_data, api_controller=api_controller)}",
        parse_mode=ParseMode.HTML,
        reply_markup=favorite_list_buttons(favorite_data=db_controller.get_all_faves(user_id=message.from_user.id),
                                           api_controller=api_controller, favorite_size=len(favorite_data)))


@route.message(Command("favorite"))
async def cmd_favorite(message: types.Message, state: FSMContext):
    await send_favorite(message)
    await state.set_state(state=None)


@route.callback_query(StateFilter(None), FavoriteCallback.filter())
async def favorite_query_handler(callback: types.CallbackQuery, callback_data: FavoriteCallback, state: FSMContext):
    film_name = callback_data.film_name
    film_id = callback_data.film_id
    api_control = api_controller.get_similar_fim(film_name)
    my_index = 0
    for index, elem in enumerate(api_control):
        if elem["nameRu"].lower() == api_control.lower():
            my_index += index
    if callback_data:
        await send_photo_with_bot(message=callback.message, user_id=callback.message.from_user.id, film_id=film_id, api_control=api_control, data=my_index)
        await state.set_state(state=None)
