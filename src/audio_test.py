import speech_recognition as sr

def speak_to_move():
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            r.adjust_for_ambient_noise(source, duration = 0.5)
            audio = r.listen(source)
            if ValueError:
                print("Please say it again")
                audio = r.listen(source)

            result = r.recognize_google(audio)
            print(result)
            commands = result.split()
            del commands[3:]
            print(commands)



speak_to_move()