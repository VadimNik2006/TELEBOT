# if __name__ == '__main__':
#     pass
from pprint import pprint
import requests
import json

# import dotenv


API_KEY = {
    "X-API-KEY": "you api"
}
USER_FILM_NAME = "Хатико"
PARAMS = {
    "keyword": USER_FILM_NAME
}


# # ses = requests.session()
# # ses.headers = API_KEY
# # #
# # #
# # def get_data(url, params):
# #     return json.loads(ses.get(url, params=params).text)
# # #
# # #
# # response_a = get_data("https://kinopoiskapiunofficial.tech/api/v2.2/films", {"keyword": USER_FILM_NAME})
# #
# # # a = requests.get("https://kinopoiskapiunofficial.tech/api/v2.2/films",
# # #                  params={"keyword": "Хатико"}, headers=API_KEY).text
# # pprint(response_a)
# # # FILM_ID = [(item["kinopoiskId"], item["nameRu"]) for item in response_a["items"]]
# #
# # FILM_ID = [ID["kinopoiskId"] for ID in response_a["items"]]
# # f = 4395219
# # FILM_NAME = [name["nameRu"] for name in response_a["items"]]
# #
# #
# # response_b = get_data(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{[i for i in FILM_ID]}/videos", params=None)
# #
# # FILM_TRAILER = [(link["url"], link["name"]) for link in response_b["items"]]
# #
# # pprint(FILM_TRAILER)
# # # pprint(response_b)
#

class APIController:
    def __init__(self, api_key):  # "Хатико"
        # self.user_film_name = user_film_name
        self.ses = requests.session()
        self.ses.headers = api_key
        # self.film_dict = dict()
        # self.film_info = json.loads(self.ses.get("https://kinopoiskapiunofficial.tech/api/v2.2/films",
        #                                          params=PARAMS).text)["items"]

    def get_similar_film(self, keyword):
        params = {
            "keyword": keyword
        }
        response = self.ses.get("https://kinopoiskapiunofficial.tech/api/v2.2/films", params=params)
        return json.loads(response.text)["items"]

    def get_film_trailer(self, films_info):
        for film_info in films_info:
            response = json.loads(self.ses.get(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_info['kinopoiskId']}/videos").text)
            film_info["trailer"] = response["items"]
        return films_info

    # def __str__(self):
    #     return


my_film = APIController(api_key=API_KEY)
pprint(my_film.get_film_trailer(my_film.get_similar_film(USER_FILM_NAME)))
