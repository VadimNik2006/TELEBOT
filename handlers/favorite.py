from pprint import pprint

from aiogram import Router

from api.controller import api_controller
from database.db_controller import db_controller
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from database.db_controller import db_controller

from keybords.cmd_favorite.favorite_inline import *
from utils import print_for_favorite_buttons, send_photo_with_bot

# from keybords.cmd_favorite.favorite_inline import favorite_list_buttons


route = Router()


def favorite_db(user_id, film_id, add=True):
    db_controller.toggle_favorite(user_id=user_id, film_id=film_id, add=add)


async def send_favorite(message: types.Message):
    favorite_data = db_controller.get_all_faves(user_id=message.from_user.id)
    await message.answer(
        text=f"<b>Избранные фильмы:</b>"
             f" {print_for_favorite_buttons(favorite_data=favorite_data, api_controller=api_controller)}",
        parse_mode=ParseMode.HTML,
        reply_markup=favorite_list_buttons(favorite_data=db_controller.get_all_faves(user_id=message.from_user.id),
                                           api_controller=api_controller, favorite_size=len(favorite_data)))


@route.message(Command("favorite"))
async def cmd_favorite(message: types.Message, state: FSMContext):
    await send_favorite(message)
    await state.set_state(state=None)


@route.callback_query(StateFilter(None), FavoriteCallback.filter())
async def favorite_query_handler(callback: types.CallbackQuery, callback_data: FavoriteCallback, state: FSMContext):
    film_id = callback_data.film_id
    film_name = api_controller.get_film_name_from_id(film_id=film_id)
    api_control = api_controller.get_similar_film(keyword=film_name)
    user_id = callback.from_user.id
    my_index = 0
    for index, elem in enumerate(api_control):
        if elem["nameRu"].lower() == api_control:
            print(my_index)
            my_index += index
    if callback_data:
        await send_photo_with_bot(message=callback.message, user_id=user_id, film_id=film_id, api_control=api_control,
                                  data=my_index,
                                  db_con=db_controller.favorite_datas_view(user_id=user_id, film_id=film_id))
        await state.set_state(state=None)


items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]


async def send_items(message: types.Message, state: FSMContext):
    current_page = await state.get_data().get('current_page', 0)
    items_per_page = 2  # Количество элементов на странице

    start_index = current_page * items_per_page
    end_index = min(start_index + items_per_page, len(items))

    pages_count = len(items) // items_per_page + (len(items) % items_per_page > 0)

    if end_index > len(items):
        end_index = len(items)

    text = "\n".join(items[start_index:end_index])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    next_button = types.InlineKeyboardButton(text="Next", callback_data="next")
    prev_button = types.InlineKeyboardButton(text="Prev", callback_data="prev")

    if current_page > 0:
        keyboard.add(prev_button)
    if current_page < pages_count - 1:
        keyboard.add(next_button)

    await message.reply(text, reply_markup=keyboard)


async def on_callback_query(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data
    current_page = await state.get_data().get('current_page', 0)

    if data == "next":
        new_page = current_page + 1
    elif data == "prev":
        new_page = max(current_page - 1, 0)
    else:
        return

    await state.update_data(current_page=new_page)
    await callback.bot.answer_callback_query(callback.id)
    await callback.bot.send_message(callback.from_user.id, "Current page updated.",
                                    reply_markup=types.InlineKeyboardMarkup())


@route.message(commands=['start'])
async def cmd_start(message: types.Message):
    await send_items(message, FSMContext())


@route.callback_query(lambda c: c.data in ["next", "prev"])
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await on_callback_query(callback_query, state)