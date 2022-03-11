#Using google's vocabulary bank as a source for recognising words
#More efficent and is far more effective than training it for every possible word outcome
#Implement in version 1 of the code
"""
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

def mic_input():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(source)
        return str(r.recognize_google(audio))


print(mic_input())
"""
