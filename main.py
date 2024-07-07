# if __name__ == '__main__':
#     pass
from pprint import pprint
import requests
import json

# import dotenv


# API_KEY = {
#     "X-API-KEY": "YOUR API KEY"
# }
API_KEY = {
    "X-API-KEY": "YOU API KEY"
}

USER_FILM_NAME = "Хатико"
PARAMS = {
    "keyword": USER_FILM_NAME
}


# ses = requests.session()
# ses.headers = API_KEY
# #
# #
# def get_data(url, params):
#     return json.loads(ses.get(url, params=params).text)
# #
# #
# response_a = get_data("https://kinopoiskapiunofficial.tech/api/v2.2/films", {"keyword": USER_FILM_NAME})
#
# # a = requests.get("https://kinopoiskapiunofficial.tech/api/v2.2/films",
# #                  params={"keyword": "Хатико"}, headers=API_KEY).text
# pprint(response_a)
# # FILM_ID = [(item["kinopoiskId"], item["nameRu"]) for item in response_a["items"]]
#
# FILM_ID = [ID["kinopoiskId"] for ID in response_a["items"]]
# f = 4395219
# FILM_NAME = [name["nameRu"] for name in response_a["items"]]
#
#
# response_b = get_data(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{[i for i in FILM_ID]}/videos", params=None)
#
# FILM_TRAILER = [(link["url"], link["name"]) for link in response_b["items"]]
#
# pprint(FILM_TRAILER)
# # pprint(response_b)


class Film:
    def __init__(self, user_film_name):  # "Хатико"
        self.user_film_name = user_film_name
        self.ses = requests.session()
        self.ses.headers = API_KEY
        self.film_info = json.loads(self.ses.get("https://kinopoiskapiunofficial.tech/api/v2.2/films",
                                                 params=PARAMS).text)["items"]

    def get_film_id(self):
        return [ID["kinopoiskId"] for ID in self.film_info]

    def get_film_name(self):
        return [name["nameRu"] for name in self.film_info]

    def get_film_trailer(self):
        for d in self.
        response = json.loads(self.ses.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{}/videos").text)

    def __str__(self):
        pass


my_film = Film(user_film_name=USER_FILM_NAME)
