from keybords.cmd_search_movie.search_inline import search_buttons
from keybords.cmd_favorite.favorite_inline import favorite_buttons
import functools
from datetime import datetime
from time import time
from aiogram import types
from pprint import pprint


def power_kb(is_search=False, is_liked=False, id=None):
    buttons = [*favorite_buttons(is_search, is_liked, id)]
    if is_search:
        buttons.insert(0, *search_buttons(id=id))
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
