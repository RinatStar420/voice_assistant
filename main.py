import speech_recognition

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка']
    }
}

def listen_command():
    """Эта функция возвращает распознанную команду"""
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            return query
    except speech_recognition.UnknownValueError:
        return 'Эм.... не помнял что ты сказал'

def greeting():
    """функция приветствия"""
    return "привет Ринатик"

def create_task():
    print('Что добавин в список дел?')

    query = listen_command()

    with open('todo-list.txt', 'a') as file:
        file.write(f'{query}\n')
    return f'Задача {query} успешно добавлено в todo-list'


def main():
    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())


if __name__ == '__main__':
    main()








