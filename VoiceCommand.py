import pyttsx3
import win32com.client
import speech_recognition as sr

speaker = win32com.client.Dispatch("SAPI.SpVoice")



def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    print("NExt")
    #speaker.Speak(text)

    engine.runAndWait()


def takeCommands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language = "en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Sorry Some error occured sir."

if __name__ == "__main__":
    say("Hello sir i am Edith, at your service")

    while True:
        print("Listening ...")
        r = takeCommands()

        say(r)
