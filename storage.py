from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from pprint import pprint

bot = Bot(token=config.bot_token.get_secret_value())

logging.basicConfig(level=logging.INFO)


dp = Dispatcher(storage=MemoryStorage())


API_KEY = {
    "X-API-KEY": config.api_key
}
USER_FILM_NAME = "Хатико"
PARAMS = {
    "keyword": USER_FILM_NAME
}



my_film = APIController(api_key=API_KEY)
pprint(my_film.get_film_trailer(my_film.get_similar_film(USER_FILM_NAME)))
