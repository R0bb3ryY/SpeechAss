# Крэк
import os
import sys
import datetime
import random
import webbrowser
import subprocess
import sympy
import requests
from fuzzywuzzy import fuzz
from num2words import num2words
from sympy.testing.runtests import sp
import openai
import speech_recognition as sr

import config
import stt
import tts

print(f"{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")
def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Что?")
        else:
            execute_cmd(cmd['cmd'])

def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    if cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "открывать браузер"
        text += "произносить статус погоды"
        tts.va_speak(text)
        pass
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейч+ас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        tts.va_speak(text)
    elif cmd == 'joke':
        jokes = ['Шутка один',
                 'Шутка два',
                 'Шутка три']
        tts.va_speak(random.choice(jokes))
    elif cmd == 'open_browser':
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open("http://python.org")
    elif cmd in ['open_explorer']:
        subprocess.call("explorer C:\\", shell=True)
    elif cmd == 'open_explorer':
        print("Открываю проводник...")  # Отладочный вывод
        open_file_explorer()
    elif cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "произносить дату ..."
        text += "рассказывать анекдоты ..."
        text += "открывать браузер ..."
        text += "открывать проводник ..."
        text += "получать прогноз погоды ..."
        text += "выполнять простые математические операции ..."
        tts.va_speak(text)
    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
        tts.va_speak(text)
    elif cmd == 'date':
        # Получаем текущую дату
        now = datetime.datetime.now()
        day = num2words(now.day, lang='ru')
        month = num2words(now.month, lang='ru')
        year = num2words(now.year, lang='ru')
        date_text = f"Сегодня {day} {month} {year} года."
        tts.va_speak(date_text)  # Произносим дату
        return date_text
    elif cmd == 'weather':
        # Получить погоду
        city = "Губкинский"  # Название города
        api_key = "nujenapi"
        try:
            # Добавляем параметр lang=ru для получения данных на русском
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru")
            response.raise_for_status()  # Проверяем статус ответа
            weather_data = response.json()
            # Отладочный вывод
            print(weather_data)  # Выводим полученные данные для проверки
            if weather_data.get("cod") == 200:
                temp = round(weather_data["main"]["temp"])  # Округление температуры
                description = weather_data["weather"][0]["description"]  # Описание погоды
                # Список для отрицательных температур
                negative_degrees_words = negative_degrees_words = [
    "ноль", "один", "два", "три", "четыре", "пять",
    "шесть", "семь", "восемь", "девять", "десять",
    "одиннадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать",
    "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать", "двадцать",
    "двадцать один", "двадцать два", "двадцать три", "двадцать четыре",
    "двадцать пять", "двадцать шесть", "двадцать семь", "двадцать восемь",
    "двадцать девять", "тридцать", "тридцать один", "тридцать два",
    "тридцать три", "тридцать четыре", "тридцать пять", "тридцать шесть",
    "тридцать семь", "тридцать восемь", "тридцать девять", "сорок", "пятьдесят", "сорок девять", "сорок восемь", "сорок семь", "сорок шесть",
    "сорок пять", "сорок четыре", "сорок три", "сорок два", "сорок один",
]

                if temp < 0 and temp >= -50:
                    degrees_word = f"минус {negative_degrees_words[abs(temp)]} градусов"
                elif temp == 0:
                    degrees_word = "ноль градусов"
                elif temp == 1:
                    degrees_word = "один градус"
                elif temp < 5:
                    degrees_word = f"{temp} градуса"
                else:
                    degrees_word = f"{temp} градусов"
                celsius_word = "Цельсия"  # Слово "Цельсия"
                text = f"Температура в {city} сейчас {degrees_word} {celsius_word} с описанием: {description}."
                tts.va_speak(text)
            else:
                tts.va_speak("Не удалось получить данные о погоде.")
        except requests.exceptions.RequestException as e:
            tts.va_speak("Произошла ошибка при получении данных о погоде. Проверьте подключение к интернету.")
            print(e)
    else:
        answer = ask(cmd)
        tts.va_speak(answer)

def open_file_explorer(path=None):
    if path is None:
        path = os.path.expanduser("~")  # Открывает домашнюю директорию
    subprocess.Popen(['explorer', path])  # Открываем проводник


def ask(question: str) -> str:
    openai.api_key = 'nujen api'
    if not isinstance(question, str):
        raise ValueError("question должен быть строкой")

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            max_tokens=100,
            temperature=0.2,
        )
        answer = completion.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return "Извините, я не могу ответить на этот вопрос."
def get_voice_input() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Пожалуйста, задайте ваш вопрос:")
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio, language='ru-RU')  # Распознаем речь с помощью Google
        print(f"Вы задали вопрос: {question}")
        return question
    except sr.UnknownValueError:
        print("Извините, не удалось распознать речь.")
        return ""
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")
        return ""

    # Пример использования
if __name__ == "__main__":
    question = get_voice_input()  # Получаем вопрос из голосового ввода
    if question:  # Проверяем, что было получено
        answer = execute_cmd(recognize_cmd(question))


word_to_number = {

    "ноль": 0,

    "один": 1,

    "два": 2,

    "три": 3,

    "четыре": 4,

    "пять": 5,

    "шесть": 6,

    "семь": 7,

    "восемь": 8,

    "девять": 9,

    "десять": 10,

    "одиннадцать": 11,

    "двенадцать": 12,

    "тринадцать": 13,

    "четырнадцать": 14,

    "пятнадцать": 15,

    "шестнадцать": 16,

    "семнадцать": 17,

    "восемнадцать": 18,

    "девятнадцать": 19,

    "двадцать": 20,

    "тридцать": 30,

    "сорок": 40,

    "пятьдесят": 50,

    "шестьдесят": 60,

    "семьдесят": 70,

    "восемьдесят": 80,

    "девяносто": 90,

    "сто": 100,

    "двести": 200,

    "триста": 300,

    "четыреста": 400,

    "пятьсот": 500,

    "шестьсот": 600,

    "семьсот": 700,

    "восемьсот": 800,

    "девятьсот": 900,

}

# начать прослушивание команд
stt.va_listen(va_respond)