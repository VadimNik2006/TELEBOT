from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from utils import send_photo_with_bot


# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from utils import print_for_favorite_buttons


class LikeCallback(CallbackData, prefix="like"):
    is_search: bool
    is_liked: bool
    id_info: int


class FavoriteCallback(CallbackData, prefix="fav"):
    film_id: int


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


def favorite_list_buttons(favorite_data, api_controller, favorite_size=None):
    keyboard = InlineKeyboardBuilder()
    print(favorite_size)
    for index, item in enumerate(favorite_data):
        cur_pages = 0
        film_name = api_controller.get_film_name_from_id(item["film_id"])
        print(film_name)
        keyboard.add(types.InlineKeyboardButton(text=film_name, callback_data=FavoriteCallback(film_id=item[
                                                                                            "film_id"]).pack()))
        # else:
        #     cur_pages += 1

    return keyboard.as_markup()

    # start = (page - 1) * row_size
        # end = page * row_size

        # index = 0
        # for item in favorite_data:
        #     film_name = api_controller.get_film_name_from_id(item["film_id"])
        #     print(film_name)
        #     if index != favorite_size:
        #         keyboard.add(types.InlineKeyboardButton(text=film_name, callback_data=FavoriteCallback(film_name=film_name,
        #                                                                                                film_id=item[
        #                                                                                                    "film_id"]).pack()))
        #         index += 1
        # return keyboard.as_markup()


async def pagination(message: types.Message, state: FSMContext, favorite_size=None):
    current_page = await state.get_data().get('current_page', 0)
    items_per_page = 5  # Количество элементов на странице

    start_index = current_page * items_per_page
    end_index = min(start_index + items_per_page, favorite_size)

    pages_count = favorite_size // items_per_page + (favorite_size % items_per_page > 0)

    if end_index > favorite_size:
        end_index = favorite_size

    text = "\n".join(items[start_index:end_index])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    next_button = types.InlineKeyboardButton(text="Next", callback_data="next")
    prev_button = types.InlineKeyboardButton(text="Prev", callback_data="prev")

    if current_page > 0:
        keyboard.add(prev_button)
    if current_page < pages_count - 1:
        keyboard.add(next_button)

    await message.reply(text, reply_markup=keyboard)


