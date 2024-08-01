from aiogram import types
from aiogram.filters.callback_data import CallbackData
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













# # Определение CallbackData для обработки нажатий кнопок
# callback_data = CallbackData("button", "action")
#
# async def create_inline_keyboard(data_list):
#     # Создание экземпляра InlineKeyboardMarkup
#     keyboard = types.InlineKeyboardMarkup()
#
#     # Итерация по списку данных и добавление кнопок
#     for data in data_list:
#         text = data.get('text')  # Получаем текст кнопки
#         action = data.get('action')  # Получаем callback_data кнопки
#         button = types.InlineKeyboardButton(text=text, callback_data=callback_data.new(action=action))
#         keyboard.add(button)
#
#     # Возвращение клавиатуры
#     return keyboard
#
# # Обработчик колбэка для кнопок
# @dp.callback_query_handler(callback_data.filter())
# async def handle_callback_button(query: types.CallbackQuery, callback_data: dict):
#     print(f"Нажата кнопка {callback_data['action']}")
#     await query.answer()
#
# # Пример использования функции создания клавиатуры
# data_list = [
#     {'text': 'Кнопка 1', 'action': 'action1'},
#     {'text': 'Кнопка 2', 'action': 'action2'}
# ]
# async def send_message_with_keyboard(chat_id: int):
#     keyboard = await create_inline_keyboard(data_list)
#     await bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)
#
# if __name__ == "__main__":
#     from aiogram import executor
#     executor.start_polling(dp)
