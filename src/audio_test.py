import speech_recognition as sr
test = ["A5", "to", "too", "2", "B6"]

def speak_to_move():
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            r.adjust_for_ambient_noise(source, duration = 0.5)
            audio = r.listen(source)
            # if ValueError:
            #     print("Please say it again")
            #     audio = r.listen(source)

            result = r.recognize_google(audio)
            print(result)
            commands = result.split()
            del commands[3:]

            for i in range(3):
                if is_legal(commands[i]) == True:
                    print("this is right")
                    continue
                else:
                    print("command is wrong")
                    return 0
            
            print(commands)

def is_legal(command):
    for i in range(5):
        if command == test[i]:
            return True
    return False

speak_to_move()