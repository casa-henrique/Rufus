import speech_recognition as sr

# Criando o reconhecedor
r = sr.Recognizer()

# Utilizando o Microfone para captura
with sr.Microphone() as source:
    while True:
        audio = r.listen(source) # Definindo o microfone como fonte de áudio
        
        print(r.recognize_google(audio, language="pt-br"))
