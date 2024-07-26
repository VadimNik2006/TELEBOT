from aiogram import types
from aiogram.filters.callback_data import CallbackData
# from utils import print_for_favorite_buttons
# from api.controller import api_controller
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from utils import print_for_favorite_buttons


class LikeCallback(CallbackData, prefix="like"):
    is_search: bool
    is_liked: bool
    id_info: int


def favorite_buttons(is_search: bool = False, is_liked: bool = False, id: int = None):
    text = "♡" if not is_liked else "❤️"
    buttons = [
        [
            types.InlineKeyboardButton(text=text,
                                       callback_data=LikeCallback(is_search=is_search, is_liked=is_liked, id_info=id).pack())
        ]
    ]
    return buttons


# for_button = print_for_favorite_buttons(favorite_data=None, api_controller=None)
#
#
#         def favorite_list_buttons(for_button):
#         text = for_button
#         builder = types.InlineKeyboardBuilder()
#         for i in text.split("\n"):
#             builder.add(types.InlineKeyboardButton, )