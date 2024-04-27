import speech_recognition as sr
from pydub import AudioSegment
import soundfile as sf


def ogg_to_wav():
    data, samplerate = sf.read('voice.ogg')
    sf.write('voice.wav', data, samplerate)


def speech_to_text():
    ogg_to_wav()
    r = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='ru-RU')
            return text
        except sr.exceptions.UnknownValueError:
            return 'Я не понял, повторите пожалуйста'