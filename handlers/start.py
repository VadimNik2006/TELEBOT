from aiogram.utils.formatting import Text, Bold
from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from keybords.cmd_start.start_inline import create_start_kb
from aiogram.enums import ParseMode
from api.controller import api_controller
from messages import messages
from states.for_start_hand import Keyword
import json
from difflib import SequenceMatcher

route = Router()


@route.message(Command("start"))
async def cmd_start(message: types.Message):
    content = Text(
        "Привет, ",
        Bold(message.from_user.username)
    )
    await message.answer(**content.as_kwargs())
    await message.answer(
        messages["start"]["main"],
        reply_markup=create_start_kb()
    )


async def send_help_message(message: types.Message):
    await message.answer(messages["help"]["main"], parse_mode=ParseMode.HTML)


@route.message(Command("help"))
async def help_command_handler(message: types.Message):
    await send_help_message(message)


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
    # print(for_check)
    for_check = (await state.get_data())["movie_vars"]

    user_message = message.text.lower()
    similarity = []

    for index, elem in enumerate(for_check):
        sim = SequenceMatcher(None, user_message, elem).ratio()
        if sim > 0.9:
            similarity.append((sim, index))

    if similarity:

        movie_index = max(similarity)[1]

        await message.answer(
            text=f"Полная информация о фильме: \n\n {json.dumps(api_controller.get_similar_film(for_check[movie_index]), indent=4)}"
        )

        await state.clear()
    else:
        await message.answer("Пожалуйста, скопируйте текст и попробуйте еще раз!")


@route.callback_query(StateFilter(None), F.data)
async def callbacks_command_start(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "commands_list":
        await send_help_message(callback.message)
    elif callback.data == "search":
        await callback.message.answer("Введите ключевое слово в названии фильма")
        await state.set_state(Keyword.wait_from_similar)
    elif callback.data == "history":
        await callback.message.edit_text(f"Итого: ")
    elif callback.data == "favorite":
        await callback.message.edit_text(f"Итого: ")
    elif callback.data == "start":
        await callback.message.edit_text(f"Итого: ")

    await callback.answer()
