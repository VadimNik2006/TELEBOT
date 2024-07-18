from aiogram import types
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils import power_kb
from api.controller import api_controller
from states.for_start_hand import Keyword
import json

from difflib import SequenceMatcher


route = Router()


@route.message(Keyword.wait_from_similar)
async def similar_chosen(message: types.Message, state: FSMContext):
    keyword = message.text.lower()
    films = api_controller.get_similar_film(keyword)

    similar_list = list(
        map(lambda x: films[films.index(x)]['nameRu'], films))
    for_print = ""
    for num, val in enumerate(similar_list):
        for_print += f"\n{num + 1}. {val}"

    if for_print:
        await message.answer(
            text=f"Найдены следующие фильмы:\n {for_print} \n\nСкопируй нужное название фильма и отправь его мне"
        )

        await state.set_data({"movie_vars": [val.lower() for val in similar_list]})

        await state.set_state(Keyword.wait_film)
    else:
        await message.answer("Вы ввели некорректное слово")


@route.message(Keyword.wait_film)
async def film_info(message: types.Message, state: FSMContext):
    for_check = (await state.get_data())["movie_vars"]
    user_message = message.text.lower()
    similarity = []

    for index, elem in enumerate(for_check):
        sim = SequenceMatcher(None, user_message, elem).ratio()
        if sim > 0.9:
            similarity.append((sim, index))

    if similarity:

        movie_index = max(similarity)[1]
        await state.set_data({"selected_movie": for_check[movie_index]})
        await message.answer(
            text="постер",
            reply_markup=power_kb(is_search=True),

        )

        await state.set_state(state=None)
    else:
        await message.answer("Пожалуйста, скопируйте текст и попробуйте еще раз!")


@route.callback_query(StateFilter(None), F.data)
async def callbacks_cmd_search_movie(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if callback.data == "full_info":
        await callback.message.answer(
            text=f"Полная информация о фильме: \n\n {json.dumps(api_controller.get_similar_film(data['selected_movie']), indent=4)}"
        )
    elif callback.data == "trailers":
        await callback.message.answer(
            text=f"Трейлеры: \n\n {json.dumps(api_controller.get_film_trailer(api_controller.get_similar_film(data['selected_movie'])))}"
        )
    elif callback.data == "like":
        await callback.message.edit_reply_markup(power_kb())
    await callback.answer()

# def wait():
#     movie_index = max(similarity)[1]
#     await message.answer(
#             text=f"Полная информация о фильме: \n\n {json.dumps(api_controller.get_similar_film(for_check[movie_index]),indent=4)}",
#             reply_markup=power_kb(is_search=True),
#
#         )
