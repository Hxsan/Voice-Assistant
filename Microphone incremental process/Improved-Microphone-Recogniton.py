import speech_recognition as sr
import threading

"""
r = sr.Recognizer()
mic = sr.Microphone()

r.dynamic_energy_threshold = True

output= {
    'transcription':'None',
    'Errors': None,
    'Reactive_Val': 0 
}

with mic as source:
    try:
        print("speak now")
        listen = r.listen(source) # ---> can be condensed into one line
        #output['transcription'] = r.recognize_google(listen)

    except sr.UnknownValueError:
        print("I didn't catch that! Please try again.")
        output['Errors'] = "UnknownValueError"
        output['transcription'] = "null"

#Recording the pitch of the user using an integer list
bitarr = listen.get_raw_data()

"""
r = sr.Recognizer()    
mic = sr.Microphone()
# new design

def voice():
    r = sr.Recognizer()
    mic = sr.Microphone()

    r.dynamic_energy_threshold = True

    with mic as source:
        try:
            print("speak now")
            listen = r.listen(source) # ---> can be condensed into one line
            print(r.recognize_google(listen))

        except sr.UnknownValueError:
            print("I didn't catch that! Please try again.")

def react():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        sound = r.listen(source)
        one = sound.get_raw_data(convert_rate=2,convert_width=2)
        for i in range(len(one)):
            curr = one[i]
            print(curr)

new1 = threading.Thread(target=voice).start()
new2 = threading.Thread(target=react).start()

class Microphone_inp():
    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
    
    def react(self):
        with mic as source:
            sound = self.r.listen(source)
            one = sound.get_raw_data(convert_rate=2,convert_width=2)
            for i in range(len(one)):
                curr = one[i]
                print(curr)
    




