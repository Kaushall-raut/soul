from openai import OpenAI
from dotenv import load_dotenv
import webbrowser
# import requests
import speech_recognition as sr
import pyttsx3 as ts
import os

load_dotenv()
recogniser=sr.Recognizer()      # used to access the functions/methods of class Recognizer

# voices= engine.getProperty('voices')

def speak(text):

    engine =ts.init('sapi5')     #  used to initialise text to speech functionality
    # engine.setProperty('voice',voices[1].id)   # to change the voice
    engine.say(text)
    engine.runAndWait()

def process_ai(cmd_input):

    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
        model="ALLaM-7B-Instruct-preview",
        messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":f"{cmd_input}"}],
        temperature=0.1,
        top_p=0.1
    )

    speak(response.choices[0].message.content)


def processed_cmd(cmds):
    cmd_input=cmds.lower()
    if cmd_input.startswith("open"):
        store=cmd_input.split(" ")
        # print(store)   just for checking
        webbrowser.open(f'https://www.{store[1]}.com')
    # elif "news" in cmd_input:
    #     API_KEY = "a00d5d78fe124eb39fc7bb1c63350837"
    #
    #     # API endpoint
    #     url = "https://newsapi.org/v2/top-headlines"
    #
    #     # Send request
    #     response = requests.get( f'https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}')
    #
    #     # Convert response to JSON
    #     data = response.json()
    #
    #     # Check status
    #     if data["status"] == "ok":
    #         articles = data["articles"]
    #
    #         for i in articles:
    #             print(i["title"])
    #             speak(i['title'])
    #     else:
    #         print("Error fetching news:", data)

    else:
        process_ai(cmd_input)

if __name__ == '__main__':     # execute only when it is run directly ,tab execute nahi hoga jab ye import kerke run ho
    speak("Initialising Soul")


    while True:
        print("recognizing")

        try :
            with sr.Microphone() as src:
                print("listening...")
                audio=recogniser.listen(src,timeout=1,phrase_time_limit=1)
                cmd =recogniser.recognize_google(audio)
                print(cmd.lower(),"listened")
                if cmd.lower()=='hello':
                    speak("ha bolo")


                    with sr.Microphone() as source:
                        audio=recogniser.listen(source)
                        cmd=recogniser.recognize_google(audio)

                        processed_cmd(cmd)
        except  Exception as e :
            print("Failed to recognise",e)
