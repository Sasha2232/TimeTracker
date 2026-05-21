Русский

Time Tracker

Чат-бот для отслеживания времени, выполненный в виде веб-приложения на Flask.

Описание проекта

Time Tracker Bot позволяет добавлять задачи, запускать таймер, отслеживать потраченное время и общаться с ботом через встроенный чат.

Используемые технологии

Python 3
Flask
SQLite (модуль sqlite3, без ORM)
HTML / CSS / JavaScript
Chart.js

Структура проекта


time_tracker_bot/
app.py           # Flask-приложение маршруты
bot_logic.py     # Логика чат-бота
database.py      # Работа с SQLite
templates/
     index.html   # Веб-интерфейс
requirements.txt
README.md


Установка нужных requirements

terminal: pip install requirements.txt

Запуск 

terminal: python app.py

Открой в браузере: http://127.0.0.1:5000

Команды бота

| Команда | Описание |
|---|---|
| /помощь | Список всех команд |
| /задачи | Все задачи |
| /сегодня | Задачи за сегодня |
| /итого | Общее время |
| /добавить название | Добавить задачу |
| /удалить id | Удалить задачу по ID |
| /инфо id | Подробности о задаче |
| /очистить | Удалить все задачи |
| /история | Последние 10 сообщений |
| /дата | Текущая дата и время |
| /статистика | Время по дням |


Пример раобты

Пользователь: /добавить Учёба
Бот:  Задача «Учёба» добавлена

Пользователь: /задачи
Бот: Все задачи:
      Учёба — 0 сек (2025-01-20)

Пользователь: /итого
Бот:  Общее время: 25 мин 10 сек

Пользователь: /статистика
Бот: Статистика по дням:
     2025-01-20: 25 мин 10 сек

English

Time Tracker

A time tracking chatbot built as a Flask web application.

Project Description

Time Tracker Bot allows you to add tasks, start a timer, track time spent, and communicate with the bot via a built-in chat.

Technologies Used

Python 3
Flask
SQLite (sqlite3 module, no ORM)
HTML / CSS / JavaScript
Chart.js


Project Structure

time_tracker_bot/
app.py # Flask application routes
bot_logic.py # Chatbot logic
database.py # Working with SQLite
templates/
index.html # Web interface
requirements.txt
README.md

Installing the necessary requirements

terminal: pip install requirements.txt

Run

terminal: python app.py

Open in a browser: http://127.0.0.1:5000

Bot Commands

| Command | Description |
|---|---|
| /help | List of all commands |
| /tasks | All tasks |
| /today | Today's tasks |
| /total | Total time |
| /add title | Add task |
| /delete id | Delete task by ID |
| /id info | Task details |
| /clear | Delete all tasks |
| /history | Last 10 messages |
| /date | Current date and time |
| /statistics | Time by day |

Example of work

User: /add Study
Bot: Task "Study" added

User: /tasks
Bot: All tasks:
Study - 0 sec (2025-01-20)

User: /total
Bot: Total time: 25 min 10 sec

User: /statistics
Bot: Daily statistics:
2025-01-20: 25 min 10 sec