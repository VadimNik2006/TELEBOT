import math
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class LikeCallback(CallbackData, prefix="like"):
    is_search: bool
    is_liked: bool
    id_info: int


class FavoriteCallback(CallbackData, prefix="fav"):
    film_id: int


class ControlsCallback(CallbackData, prefix='controls'):
    action: str
    page: int


def favorite_buttons(is_search: bool = False, is_liked: bool = False, id: int = None):
    text = "♡" if not is_liked else "❤️"
    buttons = [
        [
            types.InlineKeyboardButton(text=text,
                                       callback_data=LikeCallback(is_search=is_search, is_liked=is_liked,
                                                                  id_info=id).pack())
        ]
    ]
    return buttons


def controls_buttons(full_pages, curr_page=1):
    buttons = (
            types.InlineKeyboardButton(text="<<", callback_data=ControlsCallback(action="back", page=curr_page).pack()),
            types.InlineKeyboardButton(text=f"{curr_page}/{full_pages}",
                                       callback_data=ControlsCallback(action="page_shower", page=curr_page).pack()),
            types.InlineKeyboardButton(text=">>", callback_data=ControlsCallback(action="prev", page=curr_page).pack())
    )
    return buttons


def favorite_list_buttons(db_controller, api_controller, user_id, curr_page=1, page_size=5, reverse=False):
    favorite_data = db_controller.get_all_faves(user_id=user_id)
    full_pages = math.ceil(len(favorite_data) / page_size)
    if not reverse:
        if curr_page < 1:
            curr_page = full_pages
        if curr_page > full_pages:
            curr_page = 1
    if reverse:
        if curr_page < 1:
            curr_page = 1
        if curr_page > full_pages:
            curr_page = full_pages

    start_data = curr_page * 5 - 5
    end_data = start_data + page_size

    if curr_page <= full_pages:
        keyboard = InlineKeyboardBuilder()
        index = 1
        for item in favorite_data[start_data:end_data]:
            if index <= page_size:
                film_name = api_controller.get_film_name_from_id(item["film_id"])
                keyboard.add(types.InlineKeyboardButton(text=film_name, callback_data=FavoriteCallback(film_id=item[
                    "film_id"]).pack()))
                index += 1
            else:
                break
        keyboard = keyboard.adjust(1)
        keyboard.row(*controls_buttons(full_pages=full_pages, curr_page=curr_page))
        return keyboard.as_markup()
    raise ValueError("Превышено количество страниц")
