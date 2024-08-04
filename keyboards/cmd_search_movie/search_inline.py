from aiogram import types
from aiogram.filters.callback_data import CallbackData


class FilmCallback(CallbackData, prefix="film"):
    action: str
    id: int


def search_buttons(id):
    buttons = [
        [

            types.InlineKeyboardButton(text="полная информация",
                                       callback_data=FilmCallback(action="film_info", id=id).pack()),
            types.InlineKeyboardButton(text="трейлеры", callback_data=FilmCallback(action="trailers", id=id).pack()),
        ],
        [
            types.InlineKeyboardButton(text="посмотреть фильм",
                                       callback_data=FilmCallback(action="see_movie", id=id).pack())
        ]

    ]
    return buttons
