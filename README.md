### **Пару слов о боте:**

Мой телеграмм бот предназначен для поиска фильмов. В его функционал включены возможности просмотра фильма, полной информации о нем, а также его трейлеров. 

### **Бот имеет такие команды как:**

1. [ ]   /start - отправляет приветственное окно,  
2. [ ]   /help - выдает список команд,  
3. [ ]   /search_movie - осуществляет поиск фильмов по ключевому слову в названии (либо же по всему названию сразу, если оно было введено со 100% точностью),       
4. [ ]   /favorite - выдает список фильмов, добавленных в избранные (в избранные фильмы можно добавить во время поиска),   
5. [ ]   /history - выводит историю запросов (название фильма и дату поиска)

### **Подготовка к запуску бота:**

  1. Бот работает при помощи Kinopoisk API Unofficial и ограничивается 500 запросами в день (запросом считается любое взаимодействие, связанное с фильмом).
  Для создания своего api_key понадобиться перейти на сайт https://kinopoiskapiunofficial.tech, зарегистрироваться на нем и во вкладке "Профиль" скопировать API-ключ
  
  2. Для создания bot_token нужно перейти по ссылке https://t.me/BotFather (ссылка на BotFather - отца всех тг-ботов). После приветствия нужно отправить команду /newbot, после чего вы вводите название вашего бота, а далее username. 
  После всех действий FatherBot выдаст вам HTTP API
  
  3. В качестве БД был использован sqlite3 при sqlalchemy. Название для db_name можно дать любое
  
  4. После всех действий, нужно будет зайти в файл .env.template и вбить все вышеполученные данные в предназначенные для них поля. Затем нужно переименовать файл .env.template в .env

### **Запуск бота:**

  1. Создание виртуального окружения - venv. В терминале прописываем команду: python -m venv venv

  2. Выгрузка зависимостей бота. В терминале прописываем команду: pip install -r req.txt

  3. Запускаем venv. Прописываем команду: source ./venv/bin/activate   (macos, linux)
  
  4. Запуск бота. Прописываем команду: python main.py 
  