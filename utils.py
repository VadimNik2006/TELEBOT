from keybords.cmd_search_movie.search_inline import search_buttons
from keybords.cmd_favorite.favorite_inline import favorite_buttons
from aiogram import types
from pprint import pprint

def power_kb(is_search=False, is_liked=False):
    buttons = [*favorite_buttons(is_search, is_liked)]
    if is_search:
        buttons.insert(0, *search_buttons())
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


 # f"трейлер №{i + 1}": api_trailers[i]["url"],
 #            "название": api_trailers[i]["name"],
 #            "сайт": api_trailers[i]["site"]

# def print_film_trailers(api_trailers):
#     memory_dict = dict()
#     for i in range(len(api_trailers)):
#         memory_dict[f"трейлер №{i + 1}"] = api_trailers[i]["url"]
#         memory_dict["название"] = api_trailers[i]["name"]
#         memory_dict["сайт"]  = api_trailers[i]["site"]

def print_film_trailers(api_trailers):
    memory_dict = dict()
    for i in range(len(api_trailers)):
        memory_dict[f"трейлер №{i + 1}"] = {}
        memory_dict[f"трейлер №{i + 1}"]["ссылка"] = api_trailers[i]["url"]
        memory_dict[f"трейлер №{i + 1}"]["название"] = api_trailers[i]["name"]
        memory_dict[f"трейлер №{i + 1}"]["сайт"] = api_trailers[i]["site"]
    pprint(memory_dict)


    text = ""
    for key in memory_dict.keys():
        text += f"\n{key}:\n\n"
        for keys, values in memory_dict[key].items():
            text += f"      {keys}: {values}\n"
    pprint(text)
    return text
