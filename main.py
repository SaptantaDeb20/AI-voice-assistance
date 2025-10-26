import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from deepseek import DeepSeekAPI
import os
import json
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load API keys from environment variables
news_api_key = os.getenv("NEWS_API_KEY", "news_api_key")
your_api_key = os.getenv("YOUR_API_KEY", "your_api_key")

def speak(text):
    engine.say(text)
    engine.runAndWait()

import requests

import requests
import json

def aiprocess(command):
    # Define the API endpoint
    endpoint = "https://api.edenai.run/v2/audio/text_to_speech"

    # Set up headers with your API key
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTFjZDUzMTUtN2U2Ni00ZDQ1LWJjMjUtN2M3Njk4MmFjM2VhIiwidHlwZSI6ImFwaV90b2tlbiJ9.eN91sGZVsyxS-kp42bDFzytXCgnE42U17kYGBYsRReI",
        "Content-Type": "application/json"
    }

    # Prepare the payload
    payload = {
        "providers": "google,amazon",  # Specify the providers you want to use
        "language": "en-US",           # Specify the language
        "option": "MALE",               # Specify the voice option (if applicable)
        "text": command                 # The text to convert to speech
    }

    try:
        # Make the API request
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the response JSON
        result = response.json()

        # Check if the response contains audio data
        if 'google' in result and 'audio' in result['google']:
            return result['google']['audio']  # Return the audio URL from Google
        elif 'amazon' in result and 'audio' in result['amazon']:
            return result['amazon']['audio']  # Return the audio URL from Amazon
        else:
            return "No audio data returned."

    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"Error in eden_ai_process: {e}")
        
        # Return a user-friendly error message
        return "I'm sorry, I couldn't process that."

# Example usage
# command = "Hello, this is a test of the text-to-speech functionality."
# audio_url = aiprocess(command)
# print(audio_url)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "tell news" in c.lower():
        try:
            r = requests.get("https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=1b2c04dae2504d2db85026ab92c89e74")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Google Assistant...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=4, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "google":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("google active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")
