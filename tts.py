import torch
import sounddevice as sd
import time

# Параметры
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')  # cpu или gpu
text = "Роб!!!"

# Загрузка модели
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

# Проверка модели
if model is None:
    print("Модель не загружена.")
    exit(1)

# Функция воспроизведения
def va_speak(what: str):
    try:
        parts = what.split('..')  # Разбиение текста

        for part in parts:
            audio = model.apply_tts(text=part,
                                    speaker=speaker,
                                    sample_rate=sample_rate,
                                    put_accent=put_accent,
                                    put_yo=put_yo)

            print(f"Воспроизводится текст: {part}")
            sd.play(audio, sample_rate)
            sd.wait()  # Дождаться завершения воспроизведения
    except Exception as e:
        print(f"Ошибка при воспроизведении аудио: {e}")

# Запуск воспроизведения
if __name__ == "__main__":
    va_speak(text)