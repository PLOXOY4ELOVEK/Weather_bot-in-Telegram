import requests #БИБЛИОТЕКА ДЛЯ РАБОТЫ С API
import telebot #БИБЛИОТЕКА ДЛЯ СОЗДАНИЯ ТГ БОТА
from telebot.types import ReplyKeyboardMarkup, KeyboardButton #ИМПОРТ КЛАССОВ ИЗ ТЕЛЕБОТА ДЛЯ СОЗДАНИЯ РАБОЧЕЙ КЛАВИАТУРЫ
#пояснения не требуются...
bot = telebot.TeleBot("YOUR_TG_TOKEN")  #СОЗДАНИЕ ТГ БОТА С ТОКЕНОМ
api_token = "YOUR_API_TOKEN" #ТОКЕН API
keyboard = ReplyKeyboardMarkup(resize_keyboard=True) #СОЗДАНИЕ КЛАВИАТУРЫ
keyboard.add(KeyboardButton("Получить погоду", request_location=True)) #ДОБАВЛЕНИЕ КНОПКИ
keyboard.add(KeyboardButton("О проекте")) #ДОБАВЛЕНИЕ КНОПКИ
welcome_text = "Скажи мне какие твои координаты, и я скажу твою погоду" #ПРИВЕТСТВЕННЫЙ ТЕКСТ
about_text = "Самый легкий проект из тех, что я только делал. Накидаю сюда позже больше функционала.\nКнопка 'Получить погоду' спрашивает у пользователя его координаты, но не отправляет их в чат.\nПавлуша Дуров fix here please."
#ПОЯСНЕНИЕ К ВЕРХНЕЙ СТРОКЕ: ТЕКСТ "ОБ АВТОРЕ"(даже несмотря на то, что тут ничего нет об авторе, я не придумал, что написать)
@bot.message_handler(commands=["start", "help"]) #ФУНКЦИЯ АКТИВИРУЕТСЯ ПРИ ОТПРАВКЕ КОМАНДЫ /start В ЧАТ
def send_welcome(message): #ФУНКЦИЯ ОТПРАВКИ ПРИВЕТСТВЕННОГО СООБЩЕНИЯ(welcome_text) В ЧАТ С ПОЛЬЗОВАТЕЛЕМ
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard) #ОТПРАВКА ПРИВЕТСТВЕННОГО СООБЩЕНИЯ(welcome_text) В ЧАТ С ПОЛЬЗОВАТЕЛЕМ
@bot.message_handler(regexp=r"О проекте\.*") #РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ: В СООБЩЕНИИ ЕСТЬ "О проекте" И ДАЛЕЕ БЕСК. КОЛ-ВО ТОЧЕК ИЛИ НЕТ ТОЧЕК ВОВСЕ
def send_about(message): #ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ "ОБ АВТОРЕ" В ЧАТ С ПОЛЬЗОВАТЕЛЕМ
    bot.send_message(message.chat.id, about_text) #ОТПРАВКА СООБЩЕНИЯ "ОБ АВТОРЕ" В ЧАТ С ПОЛЬЗОВАТЕЛЕМ
#пояснения не требуются...
def get_weather(x, y): #ФУНКЦИЯ ПОЛУЧЕНИЯ ПОГОДЫ ИЗ API, ПОЛУЧАЕТ НА ВХОД КООРДИНАТЫ И ВОЗВРАЩАЕТ НАЗВАНИЕ ТЕРРИТОРИИ, ЕЕ СОСТОЯНИЕ(СОЛНЕЧНО, ПАСМУРНО И ТД), РЕАЛЬНАЯ ТЕМПЕРАТУРА,..
    URL = "https://api.openweathermap.org/data/2.5/weather" #КАК ОЩУЩАЕТСЯ ТЕМПЕРАТУРА И ВЛАЖНОСТЬ ВОЗДУХА; URL-АДРЕС API
    params = {"lat": x, "lon": y, "appid": api_token, "units": "metric", "lang": "ru"} #ПАРАМЕТРЫ: КООРДИНАТЫ(ПЕРВЫЕ 2), API ТОКЕН, ВЫВОД ТЕМПЕРАТУРЫ В ЦЕЛЬСИЯХ, ЯЗЫК
    response = requests.get(URL, params) #GET-ЗАПРОС В API
    json = response.json() #ПЕРЕВОД ЗАПРОСА В JSON ФОРМАТ
    return (json["name"], json["weather"][0]["description"], json["main"]["temp"], json["main"]["feels_like"], json["main"]["humidity"])
#ВОЗВРАЩЕНИЕ КОРТЕЖА ДАННЫХ ИЗ: НАЗВАНИЯ ТЕРРИТОРИИ, СОСТОЯНИЯ, ТЕМПЕРАТУРЫ(РЕАЛЬНОЙ И "КАК ОЩУЩАЕТСЯ") И ВЛАЖНОСТИ
@bot.message_handler(content_types=["location"]) #АКТИВИРУЕТСЯ ЕСЛИ ОТПРАВЛЯЕТСЯ ГЕОЛОКАЦИЯ В ЧАТ
def send_weather(message): #ОТПРАВЛЯЕТ ПОГОДУ В ЧАТ
    x, y = message.location.longitude, message.location.latitude #ПОЛУЧЕНИЕ КООРДИНАТ ИЗ СООБЩЕНИЯ
    name, desc, temp, feels_like, humidity = get_weather(x, y) #ПОЛУЧЕНИЕ ДАННЫХ О ПОГОДЕ ИЗ API
    desc, temp, feels_like, humidity = desc.capitalize(), int(temp), int(feels_like), int(humidity) #ОБРАБОТКА ПОЛУЧЕННЫХ ДАННЫХ
    if name == "": name = "Без имени" #ДОБАВЛЕНИЕ ИМЕНИ ТЕРРИТОРИИ(БЕЗ ЭТОЙ СТРОКИ БУДЕТ ВЫЛЕТАТЬ ОШИБКА ЕСЛИ В БД API НЕТ НАЗВАНИЯ ТЕРРИТОРИИ)
    text = f"🏙️Погода в: {name}\n ☁️{desc}\n 🌡️Температура {temp}°\n 🌡️Ощущается как {feels_like}°\n💧Влажность {humidity}%" #ТЕКСТ О ПОГОДЕ
    bot.send_message(message.chat.id, text) #ОТПРАВКА СООБЩЕНИЯ О ПОГОДЕ
bot.infinity_polling() #БОТ БЕСКОНЕЧНО МОЖЕТ ОБРАБАТЫВАТЬ СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯ