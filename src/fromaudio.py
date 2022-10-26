import speech_recognition as sr

r = sr.Recognizer()

with sr.AudioFile('./audios/garbage.wav') as source:
    
    # listen for the data (load audio to memory)
    try:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
    except Exception as e:
        print( e)