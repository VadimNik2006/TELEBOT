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
from pprint import pprint

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

        await state.update_data({"movie_vars": [val.lower() for val in similar_list]})

        await state.set_state(Keyword.wait_film)
    else:
        await message.answer("Вы ввели некорректное слово")


@route.message(Keyword.wait_film)
async def film_info(message: types.Message, state: FSMContext):

    for_check = (await state.get_data())["movie_vars"]
    user_message = message.text.lower()
    similarity = list()
    flag = False

    # check2 = ""
    # for sym in user_message:
    #     if sym.isalpha() or sym.isdigit():
    #         check2 += sym
    #
    # for i in for_check:
    #     check = ""
    #     for elem in i:
    #         if elem.isalpha() or elem.isdigit():
    #             check += elem
    #
    #     if check == check2:
    #         flag = True
    #         return flag
    # if flag:
    for index, elem in enumerate(for_check):
        sim = SequenceMatcher(None, elem, user_message).ratio()
        if sim > 0.9:
            similarity.append((sim, index))


    if similarity:

        movie_index = max(similarity)[1]
        await state.update_data({"selected_movie": for_check[movie_index]})
        # data = await state.get_data()

        keyword = message.text.lower()
        films = api_controller.get_similar_film(keyword)

        similar_list = list(
            map(lambda x: films[films.index(x)]['nameRu'].lower(), films))
        print(similar_list)

        if keyword in similar_list:


            api_control = api_controller.get_similar_film(for_check[movie_index])[0]

        # print(api_control)

        history_db(user_id=message.from_user.id, film_id=api_control["kinopoiskId"])

        await message.bot.send_photo(message.from_user.id,
                                     api_control['posterUrlPreview'],
                                     caption=api_control['nameRu'], reply_markup=power_kb(is_search=True))
        await state.set_state(state=None)
    else:
        await message.answer("Пожалуйста, скопируйте текст и попробуйте еще раз!")


@route.callback_query(StateFilter(None), LikeCallback.filter())
async def like_query_handler(callback: types.CallbackQuery, callback_data: LikeCallback, state: FSMContext):
    data = await state.get_data()
    api_control = api_controller.get_similar_film(data['selected_movie'])[0]
    is_liked = not callback_data.is_liked
    is_search = callback_data.is_search
    if is_liked:
        favorite_db(user_id=callback.message.from_user.id, film_id=api_control["kinopoiskId"])

    await callback.message.edit_reply_markup(reply_markup=power_kb(is_liked=is_liked, is_search=is_search))


@route.callback_query(StateFilter(None), F.data)
async def callbacks_cmd_search_movie(callback: types.CallbackQuery, state: FSMContext):
    api_control = api_controller.get_similar_film(callback.message.caption)
    if callback.data == "full_info":
        await callback.message.answer(
            text=f"Полная информация о фильме: \n\n{print_film_info(api_control[0])}"
        )
    elif callback.data == "trailers":

        await callback.message.answer(
            text=f"<b>Трейлеры:</b> \n{print_film_trailers(api_controller.get_film_trailer(api_control[0]['kinopoiskId']))}", parse_mode=ParseMode.HTML
        )
    await state.set_state(state=None)
    await callback.answer()
