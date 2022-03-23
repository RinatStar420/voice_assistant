"""Проект голосового помошника Антэй
Даннный помощник реализован путем ООП, и использоваинем библиотеки SpeechRecognition (библиотека распозования речи),
Selenium (поддержка всех основных браузеров) и pyttsx3 (голосовой ответ),
остальные библиотеки являются стандартными и входят в пакет питона"""


import sys
import speech_recognition
import os
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service





commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'restart_pc': ['перезагрузить компьютер'],
        'shutdown_pc': ['выключить компьютер'],
        'cancel_restart_pc': ['отмена перезагрузки'],
        'cancel_shutdown_pc': ['отмена выключения'],
        'open_browser': ['браузер'],
        'exit': ['выйти', 'завершить работу', 'выход']
    }
}

class Antei():
    def __init__(self):
        self.speaker = pyttsx3.init()
        self.speaker.setProperty('voice', 'russian')   # выбор языка (45 - Yuri)
        self.speaker.setProperty('rate', 200)  # скорость произношения
        self.sr = speech_recognition.Recognizer()  # инициализация обхекта рекогнайзер
        self.sr.pause_threshold = 0.5  # пауза между произношением

    def listen_command(self):
        """Эта функция возвращает распознанную команду"""
        try:
            with speech_recognition.Microphone() as mic:
                self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = self.sr.listen(source=mic)
                query = self.sr.recognize_google(audio_data=audio, language='ru-RU').lower()
                return query
        except speech_recognition.UnknownValueError:
            self.speaker.say('пожалуйста повтори')
            self.speaker.runAndWait()

    def greeting(self):
        """функция приветствия"""

        self.speaker.say('Привет Ринатик')
        self.speaker.runAndWait()

    def create_task(self):
        """Добавляет задачу в тодо-лист"""

        self.speaker.say('Что добавить в список?')
        self.speaker.runAndWait()

        query = self.listen_command()

        with open('todo-list.txt', 'a') as file:
            file.write(f'{query}\n')
        self.speaker.say(f'Задача {query} успешно добавлено в todo-list')
        self.speaker.runAndWait()

    def restart_pc(self):
        """Перезагрузка компьютера"""
        os.system('shutdown -r +5')  # -r это команда перезагрузки, +5 это добавление через 5 минут

        self.speaker.say('Компьютер будет перезагружен через 5 минут. Для отмены введите shutdown -c')
        self.speaker.runAndWait()

    def cancel_restart_pc(self):
        """Отмена перезагрузки компьютера"""
        os.system('shutdown -c') # -c это команда отмены перезагрузки

        self.speaker.say('Перезагрузка компьютера успешно отменена')
        self.speaker.runAndWait()

    def shutdown_pc(self):
        """Отключение ПК"""
        os.system('shutdown +5')

        self.speaker.say('Компьютер будет отключен через 5 минут')
        self.speaker.runAndWait()

    def cancel_shutdown_pc(self):
        """Отмена выключения ПК"""
        os.system('shutdown -c') # -c это команда отмены перезагрузки

        self.speaker.say('Отключение компьютера успешно отменено')
        self.speaker.runAndWait()

    def open_browser(self):
        """Открытие браузера, поиск инфо посредством гугл и поиск видео посредсвом ютуба"""

        self.speaker.say('Какую страницу открыть?')
        self.speaker.runAndWait()



        self.service = Service(executable_path='/Users/rinatrinat/Documents/chromedriver/chromedriver') # указание абсолютного пути к драйверу
        self.options = webdriver.ChromeOptions() # инициализируем объект опций
        self.options.add_experimental_option('detach', True) # позволяет держать браузер открытым после выполнения функции
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        self.driver.implicitly_wait(1)  # пауза в одну секунду
        self.driver.maximize_window() # окно на полный экран

        query = self.listen_command() # принятие ответа пользователя какую страницу он хочет открыть

        if 'гугл' in query:
            self.speaker.say('Что будем искать?')
            self.speaker.runAndWait()

            query = self.listen_command()  # слушаем команду
            query = query.split()

            self.driver.get('https://www.google.com/search?q=' + '+'.join(query))  # отправляем в гугл полученный запрос
            self.speaker.say(f'Поиск по {query} успешно запущен')
            self.speaker.runAndWait()

            return # выход из функции

        elif 'ютуб' in query:
            self.speaker.say('Что будем смотреть?')
            self.speaker.runAndWait()

            query = self.listen_command()
            query = query.split()

            self.driver.get('https://youtube.com/results?search_query=' + '+'.join(query))
            self.speaker.say('Приятного просмотре!')
            self.speaker.runAndWait()

            return  # выход из функци

        else:
            self.speaker.say('Не понятно, повторите')
            self.speaker.runAndWait()


    def exit(self):
        """Выход из голосового помощника"""
        self.speaker.say('See you soon')
        self.speaker.runAndWait()
        sys.exit()


def main():

    bot_1 = Antei()
    sr = speech_recognition.Recognizer()

    # Зацикливание бота
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

            for k, v in commands_dict['commands'].items():
                if query in v:
                    execute = getattr(bot_1, k)
                    execute()

        except Exception as _ex:
            print(_ex, 'Команда не распознана')
            sys.exit()


if __name__ == '__main__':
    main()
