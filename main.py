
import pyttsx3
import speech_recognition as sr
import pyautogui
import random

from fuzzywuzzy import fuzz


# func to talk
def speak(text):
    print(text)
    jack_voice.say(text)
    jack_voice.runAndWait()
    jack_voice.stop()

#check
def recognize_cmd(task):
    RC = {'cmd': '', 'percent': 0}
    for c, v in main_dict['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(task, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC['cmd']


#listening
def command():
    jack_heards = sr.Recognizer()

    # listen micro
    with sr.Microphone() as source:
        # pause in 1 second
        jack_heards.pause_threshold = 1
        # clean extra noise
        print("Розпізнавати....")
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

#all command
def makeSomething(task):
    if any(i in task for i in main_dict["names"]):
        for x in main_dict['names']:
            task = task.replace(x, "").strip()
        task = recognize_cmd(task)
        if task == 'yandex_song_next':
            speak(random.choice(main_dict['accomp']))
            pyautogui.hotkey('ctrl', 'l')

        elif task == 'yandex_song_back':
            speak(random.choice(main_dict['accomp']))
            pyautogui.hotkey('ctrl', 'k')
        elif task == 'yandex_song_pause':
            speak(random.choice(main_dict['accomp']))
            pyautogui.hotkey('ctrl', 'p')
        else:
            speak(random.choice(main_dict['wrong_rec']))


if __name__ == '__main__':
    # dictionarys
    main_dict = {
        # names of assistent
        "names": ('джек', 'джеки'),
        # Words that should be deleted
        "removed": ('песню', 'назад', 'поставь'),
        # commands
        "cmds": {
            "yandex_song_next": ('переключи', 'следующую'),
            "yandex_song_back": ('верни'),
            "yandex_song_pause": ('останови', 'включи музыку', 'паузу','пауза')
        },
        "accomp": ('виконувавши', 'одну секундочку', 'вже виконую', 'зараз', 'так, звичайно','буде зроблено', 'знову робота'),
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
