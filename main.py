# if __name__ == '__main__':
#     pass
from pprint import pprint
import requests
import json
import dotenv

ses = requests.session()
API_KEY = {
    "X-API-KEY": "YOUR API KEY"
}
ses.headers = API_KEY


def get_data(url, params):
    return json.loads(ses.get(url, params=params).text)


response_a = get_data("https://kinopoiskapiunofficial.tech/api/v2.2/films", {"keyword": "Хатико"})

# a = requests.get("https://kinopoiskapiunofficial.tech/api/v2.2/films",
#                  params={"keyword": "Хатико"}, headers=API_KEY).text
pprint(response_a)
FILM_ID = [(item["kinopoiskId"], item["nameRu"]) for item in response_a["items"]]

print(FILM_ID)


response_b = get_data(f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{FILM_ID}/videos", params=None)


pprint(response_b)
