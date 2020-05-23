import pyttsx3
import speech_recognition as sr
import pyautogui
import random

from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup
from config import translate_key
import requests as req


# func to talk
def speak(text):
    print(text)
    jack_voice.say(text)
    jack_voice.runAndWait()
    jack_voice.stop()


# check with fuzzywuzzy
def recognize_cmd(task):
    RC = {'cmd': '', 'percent': 0}
    for c, v in main_dict['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(task, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC['cmd']


# listening
def command():
    jack_heards = sr.Recognizer()

    # listen micro
    with sr.Microphone() as source:
        # pause in 1 second
        jack_heards.pause_threshold = 1
        # clean extra noise
        print("Розпізнавати...")
        jack_heards.adjust_for_ambient_noise(source, duration=1)
        # rec
        audio = jack_heards.listen(source)

    try:
        task = jack_heards.recognize_google(audio, language="ru-RU").lower()
        print(task)
    except sr.UnknownValueError:
        speak(random.choice(main_dict['wrong_rec']))
        task = command()

    return task


# func for tranlate russian text on uk languege
def translate_on_uk(text):
    params_translate_request = {
        "key": translate_key,  # translate key api from config
        "text": text,
        "lang": 'ru-uk'  # language from ru on uk
    }
    URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    response = req.get(URL, params=params_translate_request)
    return response.json()['text'][0]

'''
Func for parcer page with last 20 request in yandex
'''


def yandex_requst_log_cather():
    try:
        page = req.get("https://export.yandex.ru/last/last20x.xml")
    except:
        speak('Сайт впав і помер, жарти не буде')
        return
    soup = BeautifulSoup(page.text, 'lxml')
    line = soup.find('item')
    if line.text != None:
        speak('один шкіряний мішок шукає ' + translate_on_uk(line.text))
    else:
        line = soup.find('item')
        speak('один шкіряний мішок шукає ' + translate_on_uk(line.text))


# all command
def makeSomething(task):
    if any(i in task for i in main_dict["names"]):
        for x in main_dict['names']:
            task = task.replace(x, "").strip()
        task = recognize_cmd(task)
        if task == 'yandex_song_next':
            speak(random.choice(main_dict['accomp']))
            pyautogui.keyDown('ctrl')
            pyautogui.press('l')
            pyautogui.keyUp('ctrl')

        elif task == 'yandex_song_back':
            speak(random.choice(main_dict['accomp']))
            pyautogui.keyDown('ctrl')
            pyautogui.press('k')
            pyautogui.keyUp('ctrl')

        elif task == 'yandex_song_pause':
            speak(random.choice(main_dict['accomp']))
            pyautogui.keyDown('ctrl')
            pyautogui.press('p')
            pyautogui.keyUp('ctrl')
        elif task == 'yandex_request_log':
            speak(random.choice(main_dict['accomp']))
            yandex_requst_log_cather()
        else:
            speak(random.choice(main_dict['wrong_rec']))


if __name__ == '__main__':
    # dictionarys
    main_dict = {
        # names of assistent
        "names": ('джек', 'джеки'),
        # Words that should be deleted
        "removed": ('песню', 'поставь', 'что', 'яндекс', 'яндексе', 'люди'),
        # commands
        "cmds": {
            "yandex_song_next": ('переключи', 'следующую'),
            "yandex_song_back": ('верни', 'перемотай', 'назад'),
            "yandex_song_pause": ('останови', 'включи музыку', 'паузу', 'пауза'),
            'yandex_request_log': ('гуглят', 'ищут')
        },
        "accomp": (
            'виконувавши', 'одну секундочку', 'вже виконую', 'зараз', 'так, звичайно', 'буде зроблено', 'знову робота'),
        "wrong_rec": ('Ти можеш сказати це з виразом, в одному тоні', 'Ну це просто пісна хуйня якась, блядь',
                      'Давай по новій, Міша, все хуйня.', 'нічого не зрозумів, але дуже цікаво',
                      'не зрозумію, що ти мовчиш',
                      'а тепер давай розберемо по частинах тобою сказане',
                      'якщо ти щось говорив, то я ніхуя не зрозумів')

    }

    jack_voice = pyttsx3.init()

    # set ukraine voice to jack
    all_voice = jack_voice.getProperty('voices')
    jack_voice.setProperty('voice', "uk")
    for voice in all_voice:
        if voice.name == 'Anatol':
            jack_voice.setProperty('voice', voice.id)
    speak("Вітаю тебе, дурник")
    speak("Джек слухає")

    while True:
        makeSomething(command())
