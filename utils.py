import functools
from datetime import datetime
from time import time
from aiogram import types


def power_kb(is_search=False, is_liked=False, id=None):
    from keyboards.cmd_search_movie.search_inline import search_buttons
    from keyboards.cmd_favorite.favorite_inline import favorite_buttons
    buttons = [*favorite_buttons(is_search, is_liked, id)]
    if is_search:
        res = search_buttons(id=id)
        for i in range(len(res)):
            buttons.insert(i, res[i])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def print_film_info(api_film_info):
    memory_dict = {
        "название фильма": api_film_info["nameRu"],
        "страна": api_film_info["countries"][0]["country"],
        "год": api_film_info["year"],
        "жанр": api_film_info["genres"][0]["genre"],
        "рейтинг Кинопоиск": api_film_info["ratingKinopoisk"],
        "рейтинг Imdb": api_film_info["ratingImdb"]
    }

    text = ""
    for key, value in memory_dict.items():
        text += f"{key}: {value}\n"

    return text


def print_film_trailers(api_trailers):
    memory_dict = dict()
    for i in range(len(api_trailers)):
        memory_dict[f"трейлер №{i + 1}"] = {}
        memory_dict[f"трейлер №{i + 1}"]["ссылка"] = api_trailers[i]["url"]
        memory_dict[f"трейлер №{i + 1}"]["название"] = api_trailers[i]["name"]
        memory_dict[f"трейлер №{i + 1}"]["сайт"] = api_trailers[i]["site"]

    text = ""
    for key in memory_dict.keys():
        text += f"\n      {key}:\n\n"
        for keys, values in memory_dict[key].items():
            text += f"            {keys}: {values}\n"

    return text


def print_see_movie(api_see_movie):
    memory_dict = dict()
    for i in range(len(api_see_movie)):
        memory_dict[f'сайт №{i + 1}'] = api_see_movie[i]['url']

    text = ''
    for key, val in memory_dict.items():
        text += f'{key}: {val}\n\n'

    return text


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper


def format_time():
    return datetime.fromtimestamp(int(str(time()).split(".")[0]))


def print_history(history_data, api_controller):
    text = "\n\n"
    for i in history_data:
        for key, value in i.items():
            if key == "film_id":
                text += f'Название фильма: "{api_controller.get_film_name_from_id(value)}"\n'
            if key == "date":
                text += f"Время запроса: {', '.join(str(value).split())}\n"

        text += "\n"
    return text


def print_for_favorite_buttons(favorite_data, api_controller):
    text = "\n\n"
    for i in favorite_data:
        for key, value in i.items():
            if key == "film_id":
                text += f'Название фильма: "{api_controller.get_film_name_from_id(value)}"\n'

        text += "\n"
    return text


async def send_photo_with_bot(message: types.Message, user_id, api_control, data, film_id, db_con=None):
    await message.bot.send_photo(user_id,
                                 api_control[data]['posterUrlPreview'],
                                 caption=api_control[data]['nameRu'],
                                 reply_markup=power_kb(is_search=True,
                                                       is_liked=db_con,
                                                       id=film_id))
