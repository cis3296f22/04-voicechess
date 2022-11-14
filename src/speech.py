import speech_recognition as sr

chess_positions = ["A1","A2","A3","A4","A5","A6","A7","A8",
                    "B1","B2","B3","B4","B5","B6","B7","B8",
                    "C1","C2","C3","C4","C5","C6","C7","C8",
                    "D1","D2","D3","D4","D5","D6","D7","D8",
                    "E1","E2","E3","E4","E5","E6","E7","E8",
                    "F1","F2","F3","F4","F5","F6","F7","F8",
                    "G1","G2","G3","G4","G5","G6","G7","G8",
                    "H1","H2","H3","H4","H5","H6","H7","H8"]

chess_move = ["to", "To", "too", "Too", "2", "top"]

def speak_to_move():
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            if ValueError:
                print("Please say it again")
                audio = r.listen(source)
            result = r.recognize_google(audio)
            commands = result.split()
            del commands[3:]
            print(commands)

            if is_legal_position(commands[1]) == False:
                return False

            if is_legal_move(commands[2]) == False:
                return False

            if is_legal_position(commands[3]) == False:
                return False
        
        return commands
    

def is_legal_position(command):
    for i in range(64):
        if command == chess_positions[i-1]:
            return True
    return False
    
def is_legal_move(command):
    for i in range(6):
        if command == chess_move[i-1]:
            return True
    return False
    
