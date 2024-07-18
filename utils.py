from keybords.cmd_search_movie.search_inline import search_buttons
from keybords.cmd_favorite.favorite_inline import favorite_buttons
from aiogram import types


def power_kb(is_search=False):
    buttons = [*favorite_buttons()]
    if is_search:
        buttons.insert(0, *search_buttons())
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
