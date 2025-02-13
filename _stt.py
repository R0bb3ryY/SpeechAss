import time
from glob import glob

import speech_recognition as sr
import torch

device = torch.device('cpu')

# Загрузка модели Silero STT
model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en',  # en, ru
                                       device=device)
(read_batch, split_into_batches, read_audio, prepare_model_input) = utils


def callback(_r, audio):
    try:
        print("Распознание ...")

        # Получение raw аудио данных
        wav_raw = audio.get_wav_data()

        # Прямо используем данные для модели, минуя временные файлы
        input = prepare_model_input(read_batch([wav_raw]), device=device)

        # Прогон данных через модель
        output = model(input)
        for example in output:
            print(decoder(example.cpu()))

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except Exception as e:
        print(f"[log] Произошла ошибка: {e}")


# Запуск
r = sr.Recognizer()
r.pause_threshold = 0.5
m = sr.Microphone(device_index=1)

with m as source:
    print("Настройка уровня фонового шума... Пожалуйста, подождите.")
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)
print("Прослушивание начинается... Нажмите Ctrl+C для остановки.")
while True:
    time.sleep(0.1)