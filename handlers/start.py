from aiogram.utils.formatting import Text, Bold
from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from handlers.help import send_help_message
from keybords.cmd_start.start_inline import create_start_kb, MenuCallback
from messages import messages
from states.for_start_hand import Keyword


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


@route.callback_query(StateFilter(None), MenuCallback.filter())
async def callbacks_command_start(callback: types.CallbackQuery, callback_data: MenuCallback, state: FSMContext):
    if callback_data.section == "commands_list":
        await send_help_message(callback.message)
    elif callback_data.section == "search":
        await callback.message.answer("Введите ключевое слово в названии фильма")
        await state.set_state(Keyword.wait_from_similar)
    elif callback_data.section == "history":
        await callback.message.edit_text(f"Итого: ")
    elif callback_data.section == "favorite":
        await callback.message.edit_text(f"Итого: ")
    # elif callback.data == "start":
    #     await callback.message.edit_text(f"Итого: ")

    await callback.answer()
