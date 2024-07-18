from aiogram.utils.formatting import Text, Bold
from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from keybords.cmd_start.start_inline import create_start_kb
from keybords.cmd_favorite.favorite_inline import create_favorite_kb
from aiogram.enums import ParseMode
from api.controller import api_controller
from messages import messages
from states.for_start_hand import Keyword
import json
from difflib import SequenceMatcher


route = Router()


@route.message(Command("history"))
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