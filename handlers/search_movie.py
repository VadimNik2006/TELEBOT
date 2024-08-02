from aiogram.enums import ParseMode
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils import *
from api.controller import api_controller
from states.for_search_movie_hand import Keyword
from handlers.history import history_db
from handlers.favorite import favorite_db
from keybords.cmd_favorite.favorite_inline import LikeCallback
from keybords.cmd_search_movie.search_inline import FilmCallback
from database.db_controller import db_controller
from pprint import pprint


route = Router()


@route.message(Keyword.wait_from_similar)
async def similar_chosen(message: types.Message, state: FSMContext):
    keyword = message.text.lower()
    films = api_controller.get_similar_film(keyword)
    similar_list = list(
        map(lambda x: films[films.index(x)]['nameRu'], films))
    await state.update_data({"similar_list": similar_list})
    for_print = ""
    for num, val in enumerate(similar_list):
        for_print += f"\n{num + 1}. {val}"
    if for_print:
        await message.answer(
            text=f"Найдены следующие фильмы:\n {for_print} \n\nОтправьте цифру/число номера интересующего Вас фильма"
        )

        await state.set_state(Keyword.wait_film)
    else:
        await message.answer("Вы ввели некорректное слово. Введите новое слово")


@route.message(Keyword.wait_film)
async def film_info(message: types.Message, state: FSMContext):
    try:
        user_message = int(message.text)
        data = user_message - 1
        prev_movies = (await state.get_data())['similar_list']

        if 0 <= user_message <= len(prev_movies):

            api_control = api_controller.get_similar_film(prev_movies[data])
            store = []

            for index, elem in enumerate(api_control):
                if elem["nameRu"].lower() == prev_movies[data].lower():
                    store.extend([index, elem])

            data = store[0]
            user_id = message.from_user.id
            film_id = api_control[data]["kinopoiskId"]
            history_db(user_id=user_id, film_id=film_id)

            await send_photo_with_bot(message=message, film_id=film_id, user_id=user_id, data=data,
                                      api_control=api_control,
                                      db_con=db_controller.favorite_datas_view(user_id=user_id, film_id=film_id))

            await state.set_state(state=None)
        else:
            await message.answer("Ваша цифра/число находится вне диапазона количества фильмов")
    except ValueError:
        if isinstance(message.text, str) and message.text.isalpha():
            await message.answer("Пожалуйста, введите цифру/число, а не строку!")
        elif not message.text.isalpha():
            await message.answer("Вы ввели что-то непонятное. Пожалуйста, введите цифру/число!")


@route.callback_query(StateFilter(None), LikeCallback.filter())
async def like_query_handler(callback: types.CallbackQuery, callback_data: LikeCallback, state: FSMContext):
    is_liked = not callback_data.is_liked
    is_search = callback_data.is_search
    id_info = callback_data.id_info
    favorite_db(user_id=callback.from_user.id, film_id=id_info, add=is_liked)
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
