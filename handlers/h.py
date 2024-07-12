# from aiogram import Router, types
# from api.controller import api_controller
# from aiogram.filters.command import Command
# from aiogram import Dispatcher
# from aiogram.utils.formatting import Text, Bold
# from aiogram.enums import ParseMode
#
# route = Router()
#
#
# @route.message(Command("start"))
# async def cmd_start(message: types.Message):
#     content = Text(
#         "Привет, ",
#         Bold(message.from_user.username)
#     )
#     # {"text": "Привет, **Вася пупкин**", "parse_mode": 'MARKDOWN2', 'entities': []}
#     await message.answer(**content.as_kwargs())
#
#
# @route.message()
# async def echo_handler(message: types.Message):
#     await message.reply(message.text)
