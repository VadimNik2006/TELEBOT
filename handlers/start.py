from aiogram.utils.formatting import Text, Bold
from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from handlers.help import send_help_message
from database.db_controller import db_controller
from keybords.cmd_start.start_inline import create_start_kb, MenuCallback
from messages import messages
from states.for_search_movie_hand import Keyword
# from states.for_favorite_hand import Keyword2
from typing import Union

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


@route.callback_query(MenuCallback.filter())
async def callbacks_command_start(callback: types.CallbackQuery, callback_data: MenuCallback, state: FSMContext):
    await call_command(callback, state, callback_data.section)


@route.message(Command(commands=["help", "search_movie", "favorite"]))
async def base_commands_handler(message: types.Message, state: FSMContext):
    await call_command(message, state, message.text[1:])


async def call_command(update: Union[types.CallbackQuery, types.Message], state: FSMContext, command: str):
    if isinstance(update, types.CallbackQuery):
        message = update.message
    else:
        message = update

    if command == "help":
        await send_help_message(message)
    elif command == "search_movie":
        await message.answer("Введите ключевое слово в названии фильма")
        await state.set_state(Keyword.wait_from_similar)
    # elif command == "history":
    #     await message.answer(f"datas = {db_controller.get_all_history()}")
    #     # await message.edit_text(f"Итого: ")
    # elif command == "favorite":
    #     pass
        # await state.set_state(Keyword2.add_to_fav)
