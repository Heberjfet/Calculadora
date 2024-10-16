import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

for voice in voices:
    if 'Español' in voice.id or 'spanish' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Instrucciones de voz a las que reacciona
instrucciones = {
    "más": "+",
    "menos": "-",
    "asterisco": "*",
    "diagonal": "/",
    "paréntesis izquierdo": "(",
    "paréntesis derecho": ")",
    "número uno": "1",
    "número dos": "2",
    "número tres": "3",
    "número cuatro": "4",
    "número cinco": "5",
    "número seis": "6",
    "número siete": "7",
    "número ocho": "8",
    "número nueve": "9",
    "cero": "0",
    "logaritmo de": "log("
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

        try:
            print("Reconociendo...")
            text = recognizer.recognize_google(audio, language='es-ES')
            print(f"Texto reconocido: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return ""
        except sr.RequestError as e:
            print(f"Error al solicitar resultados; {e}")
            return ""

def procesarInstruccion(instruccion):
    if instruccion.isdigit():
        return instruccion
    return instrucciones.get(instruccion, "")

if __name__ == "__main__":
    expresion=""
    speak("Diga su instrucción")

    while True:
        instruccion=listen()
        if instruccion == "igual":
            speak("Ok, saliendo entonces")
            break
        elif instruccion == "borrar":
            if expresion:
                expresion = expresion[:-1]
                print(f"Expresión actual: {expresion}")
                speak("Último carácter borrado")
            else:
                speak("No hay nada que borrar")

        elif instruccion:
            char=procesarInstruccion(instruccion)
            if char:
                expresion+=char
                print(f"Expresión actual: {expresion}")
                speak(f"Agregado: {char}")
            else:
                speak("No te entendí we")
    print(f"Expresión final: {expresion}")