from aiogram.enums import ParseMode
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils import *
from api.controller import api_controller
from states.for_search_movie_hand import Keyword
from handlers.history import history_db
from handlers.favorite import favorite_db
from difflib import SequenceMatcher
from keybords.cmd_favorite.favorite_inline import LikeCallback
from keybords.cmd_search_movie.search_inline import FilmCallback
from database.db_controller import db_controller
from pprint import pprint

route = Router()


@route.message(Keyword.wait_from_similar)
async def similar_chosen(message: types.Message, state: FSMContext):
    keyword = message.text.lower()
    films = api_controller.get_similar_film(keyword.split())
    similar_list = list(
        map(lambda x: films[films.index(x)]['nameRu'], films))
    await state.update_data({"similar_list": similar_list})
    for_print = ""
    for num, val in enumerate(similar_list):
        for_print += f"\n{num + 1}. {val}"
    if for_print:
        await message.answer(
            text=f"Найдены следующие фильмы:\n {for_print} \n\nСкопируй нужное название фильма и отправь его мне"
        )

        await state.update_data({"movie_vars": [val.lower() for val in similar_list]})

        await state.set_state(Keyword.wait_film)
    else:
        await message.answer("Вы ввели некорректное слово. Введите новое слово")


@route.message(Keyword.wait_film)
async def film_info(message: types.Message, state: FSMContext):

    for_check = (await state.get_data())["movie_vars"]
    user_message = message.text.lower()
    similarity = list()

    for index, elem in enumerate(for_check):
        sim = SequenceMatcher(None, elem, user_message).ratio()
        if sim > 0.9:
            similarity.append((sim, index))

    if similarity:
        movie_index = max(similarity)[1]
        api_control = api_controller.get_similar_film(for_check[movie_index])
        await state.update_data({"api_con": api_control})
        for index, elem in enumerate(api_control):
            if elem["nameRu"].lower() == for_check[movie_index]:
                await state.update_data({"selected_movie": (index, elem)})

        data = (await state.get_data())["selected_movie"][0]
        user_id = message.from_user.id
        film_id = api_control[data]["kinopoiskId"]
        history_db(user_id=user_id, film_id=film_id)
        await message.bot.send_photo(user_id,
                                     api_control[data]['posterUrlPreview'],
                                     caption=api_control[data]['nameRu'], reply_markup=power_kb(is_search=True, id=film_id))
        await state.set_state(state=None)
    else:
        await message.answer("Пожалуйста, скопируйте текст и попробуйте еще раз!")


@route.callback_query(StateFilter(None), LikeCallback.filter())
async def like_query_handler(callback: types.CallbackQuery, callback_data: LikeCallback, state: FSMContext):
    # data = (await state.get_data())["selected_movie"][0]
    #
    # api_control = (await state.get_data())["api_con"]
    api_control = api_controller.get_similar_film(callback.message.caption.lower())
    data = 0
    for index, elem in enumerate(api_control):
        if elem["nameRu"].lower() == callback.message.caption.lower():
            data = index
            break
    is_liked = not callback_data.is_liked
    is_search = callback_data.is_search
    id_info = callback_data.id_info
    if is_liked:
        favorite_db(user_id=callback.message.from_user.id, film_id=api_control[data]["kinopoiskId"])

    await callback.message.edit_reply_markup(reply_markup=power_kb(is_liked=is_liked, is_search=is_search, id=id_info))
    await state.set_state(state=None)


@route.callback_query(StateFilter(None), FilmCallback.filter())
async def callbacks_cmd_search_movie(callback: types.CallbackQuery, callback_data: FilmCallback, state: FSMContext):
    api_control = api_controller.get_similar_film(callback.message.caption.lower())
    data = 0
    for index, elem in enumerate(api_control):
        if elem["nameRu"].lower() == callback.message.caption.lower():
            data = index
            break

    action = callback_data.action
    id_info = callback_data.id
    if action == "film_info":
        await callback.message.answer(
            text=f"Полная информация о фильме: \n\n{print_film_info(api_control[data])}"
        )
    elif action == "trailers":
        await callback.message.answer(
            text=f"<b>Название фильма:"
                 f"\n\n      {api_control[data]['nameRu']}"
                 f"\n\nТрейлеры:</b>"
                 f"\n{print_film_trailers(api_trailers=api_controller.get_film_trailer(id_info))}",
            parse_mode=ParseMode.HTML
        )
    await state.set_state(state=None)
