import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia

wake_word = "Soee"
listener = sr.Recognizer()
engine = pyttsx3.init()

# Configuración de la voz en español
engine.setProperty('voice', 'spanish')

def talk(text, action=None):
    full_text = f"{action}. {text}" if action else text
    print(full_text)
    engine.say(full_text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source, duration=0.7)
        pc = listener.listen(source, timeout=5)

    try:
        rec = listener.recognize_google(pc, language="es").lower()
        print("Texto detectado:", rec)
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
        return None

    if wake_word in rec and ('reproduce' in rec or 'busca' in rec):
        rec = rec.replace(wake_word, '').replace('reproduce', '').replace('busca', '').strip()

    return rec

# Funciones específicas para cada acción
def reproduce_accion(query):
    talk(f"Reproduciendo {query}", action="Reproduciendo")

def busca_accion(query):
    talk(f"Buscando información de {query} en Wikipedia", action="Buscando en Wikipedia")
    resultado = buscar_en_wikipedia(query)
    print(resultado)
    talk(resultado)

def otra_accion():
    # Define más funciones aquí según sea necesario
    pass

# Nueva función para buscar en Wikipedia
def buscar_en_wikipedia(consulta):
    try:
        # Configura Wikipedia para buscar en español
        wikipedia.set_lang("es")
        result = wikipedia.summary(consulta, sentences=1)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        # Si hay varias opciones de desambiguación, toma la primera opción
        result = wikipedia.summary(e.options[0], sentences=1)
        return result
    except wikipedia.exceptions.PageError:
        return f"No se encontró información para '{consulta}' en Wikipedia."

def run_Soee():
    while True:
        try:
            rec = listen()
            if rec is not None:
                if 'reproduce' in rec:
                    rec = rec.replace('reproduce', '').strip()
                    reproduce_accion(rec)
                elif 'busca' in rec:
                    rec = rec.replace('busca', '').strip()
                    busca_accion(rec)
                elif 'otra_accion' in rec:
                    otra_accion()
                # Añade más casos según sea necesario
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue

        try:
            rec = listen()
            if rec is not None:
                if 'detente' in rec:
                    print("Bot detenido.")
                    break
                else:
                    print("Bot sigue escuchando:", rec)
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue

if __name__ == '__main__':
    run_Soee()
