import speech_recognition as sr

chess_positions = ["A1","A2","A3","A4","A5","A6","A7","A8",
                    "B1","B2","B3","B4","B5","B6","B7","B8",
                    "C1","C2","C3","C4","C5","C6","C7","C8",
                    "D1","D2","D3","D4","D5","D6","D7","D8",
                    "E1","E2","E3","E4","E5","E6","E7","E8",
                    "F1","F2","F3","F4","F5","F6","F7","F8",
                    "G1","G2","G3","G4","G5","G6","G7","G8",
                    "H1","H2","H3","H4","H5","H6","H7","H8",
                    "to", "To", "too", "Too", "2", "top"]

def speak_to_move():
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source)
            except ValueError:
                print("Please say it again")
                audio = r.listen(source)
            except IndexError:
                print("Please say it again")
                audio = r.listen(source)
            result = r.recognize_google(audio)
            
            print(result)
            caps = result.upper()
            commands = caps.split()
    
            size = len(commands)

            if size < 2:
                return False
            
            if size == 3:
                del commands[1]

            del commands[3:]
            print(commands)

            for i in range(3):
                if is_legal(commands[i-1]) == True:
                    continue
                else:
                    return False
        
        return commands
    

def is_legal(command):
    for i in range(70):
        if command == chess_positions[i-1]:
            return True
    return False
    
