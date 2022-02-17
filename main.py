import argparse
import speech_recognition as sr
import os
import sounddevice as sd
import queue
import vosk
import sys
import pyttsx3
import json
import core


# SINTESE DE FALA
engine = pyttsx3.init()

voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[-2].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

'''
# RECONHECIMENTO ONLINE COM O GOOGLE

# Criando o reconhecedor
r = sr.Recognizer()

# Utilizando o Microfone para captura
with sr.Microphone() as source:
    while True:
        audio = r.listen(source) # Definindo o microfone como fonte de áudio
        
        print(r.recognize_google(audio, language="pt-br"))
'''


# RECONHECIMENTO OFFLINE
q = queue.Queue()

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)

            #Loop do reconhecimento de fala
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result = json.loads(result)

                    if result is not None:
                        text = result['text']

                        print(text)

                        if text == 'que horas são' or text == 'me diga que horas são':
                            speak(core.SystemInfo.get_time())
                        if text == 'que dia é hoje' or text == 'em que mês estamos':
                            speak(core.SystemInfo.get_day())
                        if text == 'obrigado' or 'obrigada':

                            speak(core.SystemInfo.get_congratulations())
except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
