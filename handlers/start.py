from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from keybords.inline_kb import create_start_kb

route = Router()


@route.message(Command("start"))
async def cmd_start(message: types.Message):
    content = Text(
        "Привет, ",
        Bold(message.from_user.username)
    )
    await message.answer(**content.as_kwargs())
    await message.answer(
        "\nЯ - бот, который поможет тебе подобрать любой интересующий тебя фильм"
        "\nСписок моих команд представлен ниже:",
        reply_markup=create_start_kb()
    )

# inline buttons under bots answer with commands
