"""Скрипт выборки языка в библиотеке pyttsx3"""

import pyttsx3

speaker = pyttsx3.init()
voices = speaker.getProperty('voices')   # список изь доступных голосов

for index, voice in enumerate(voices):
    print(f'Index: {index}\nVoice: {voice.name}\n{"#"*20}')

speaker.setProperty('voice', voices[1])
speaker.setProperty('rate', 200)
speaker.say('привет')
speaker.runAndWait()