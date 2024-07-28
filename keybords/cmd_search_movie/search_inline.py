from aiogram import types
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix="film"):
    action: str
    id: int


def search_buttons(id):
    buttons = [
        [
            types.InlineKeyboardButton(text="полная информация", callback_data=FilmCallback(action="film_info", id=id).pack()),
            types.InlineKeyboardButton(text="трейлеры", callback_data=FilmCallback(action="trailers", id=id).pack()),
        ]
    ]
    return buttons
# def search_buttons(id):
#     buttons = [
#         [
#             types.InlineKeyboardButton(text="полная информация", callback_data="full_info"),
#             types.InlineKeyboardButton(text="трейлеры", callback_data="trailers"),
#         ]
#     ]
#     return buttons


# def create_search_kb():
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=search_buttons())
#     return keyboard
