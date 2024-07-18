from aiogram import types
from aiogram import Router
from aiogram.filters import Command
from aiogram.enums import ParseMode
from messages import messages


route = Router()


async def send_help_message(message: types.Message):
    await message.answer(messages["help"]["main"], parse_mode=ParseMode.HTML)


@route.message(Command("help"))
async def help_command_handler(message: types.Message):
    await send_help_message(message)
