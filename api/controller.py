import json
import requests
import config_reader
from utils import singleton


@singleton
class APIController:
    def __init__(self, api_key):
        self.ses = requests.session()
        self.ses.headers = {'X-API-KEY': api_key.get_secret_value()}

    def get_similar_film(self, keyword):
        params = {
            "keyword": keyword
        }
        response = self.ses.get("https://kinopoiskapiunofficial.tech/api/v2.2/films", params=params)
        return json.loads(response.text)["items"]

    def get_film_trailer(self, film_id):
        response = json.loads(self.ses.get(
            f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}/videos").text)
        return response["items"]

    def get_film_name_from_id(self, film_id):
        response = json.loads(self.ses.get(
            f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}").text)
        return response["nameRu"]


api_controller = APIController(api_key=config_reader.config.api_key)
