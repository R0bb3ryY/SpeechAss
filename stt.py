import vosk
import sys
import sounddevice as sd
import queue
import json

# Загрузка модели
model = vosk.Model("model_small")
samplerate = 16000
device = 1  # Убедитесь, что это корректное устройство

q = queue.Queue()

def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    callback(json.loads(rec.Result())["text"])
                else:
                    print(rec.PartialResult())  # Показываем промежуточный результат
        except KeyboardInterrupt:
            print("Stopped by user")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    va_listen(lambda text: print(f"Распознанный текст: {text}"))