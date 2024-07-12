import json
import requests
import functools
import config_reader


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class APIController:
    def __init__(self, api_key):
        self.ses = requests.session()
        self.ses.headers = api_key

    def get_similar_film(self, keyword):
        params = {
            "keyword": keyword
        }
        response = self.ses.get("https://kinopoiskapiunofficial.tech/api/v2.2/films", params=params)
        return json.loads(response.text)["items"]

    def get_film_trailer(self, films_info):
        for film_info in films_info:
            response = json.loads(self.ses.get(
                f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_info['kinopoiskId']}/videos").text)
            film_info["trailer"] = response["items"]
        return films_info


api_controller = APIController(config_reader.config.api_key)
