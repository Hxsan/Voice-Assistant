import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()  #---> can be placed inside a class to remove global attributes

class microphone_obj(object):
    def __call__(self, r, mic):
        arr = []
        r = sr.Recognizer()
        mic = sr.Microphone()

        r.dynamic_energy_threshold = True
        
        output= {
            'transcription':'None',
            'Errors': None
        }

        with mic as source:
            try:
                print("speak now")
                listen = r.listen(source) # ---> can be condensed into one line
                output['transcription'] = r.recognize_google(listen)

            except sr.UnknownValueError:
                print("I didn't catch that! Please try again.")
                output['Errors'] = "UnknownValueError"
                output['transcription'] = "null"
        
        #Recording the pitch of the user using an integer list
        bitarr = listen.get_raw_data(convert_rate= 2, convert_width= 3)
        intarr = []
        for countA in range(len(bitarr)):
            intarr.append(bitarr[countA])

        for countB in range(len(intarr)):
            curr = intarr[countB]
        return print(output)

microphone = microphone_obj()
microphone(r,mic)