import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from deep_translator import GoogleTranslator


OPENROUTER_API_KEY = "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"  
NEWS_API_KEY = "f292fa64443a419883673fb247a3ce08"
WEATHER_API_KEY = "4b6c73978c524c1dadf134951250307" 

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    
    print(f"Bug: {text}")
    engine.say(text)
    engine.runAndWait()

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            speak("No news found.")
            return
        speak("Here are the top news headlines.")
        for article in articles[:5]:
            speak(article['title'])
    except Exception as e:
        speak("Failed to fetch news.")
        print(f"News Error: {e}")


def get_weather(cityy):
    try:
        city=cityy
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(url)
        data = response.json()
        condition = data["current"]["condition"]["text"]
        temp_c = data["current"]["temp_c"]
        speak(f"The weather in {city} is {condition} with a temperature of {temp_c} degree Celsius.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather right now.")
        print(f"Weather Error: {e}")



def translate_text(text, dest_lang="en"):
    try:
        translated = GoogleTranslator(source='auto', target=dest_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return "Translation failed"

def get_ai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant named Bug created by Adarsh and Humza. Keep answers short and clear."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenRouter API Error: {e}")
        return "Sorry, I couldn't connect to the AI service."

def processCommand(comm):
    comm = comm.lower()
    if "open google" in comm:
        speak("Opening Google...")
        webbrowser.open("https://google.com")

    elif "open facebook" in comm:
        speak("Opening Facebook...")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in comm:
        speak("Opening YouTube...")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in comm:
        speak("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")

    elif "news" in comm:
        get_news()

    elif "weather" in comm:
        speak("Tell me which city weather you need to know?..")
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                
                cityname = r.recognize_google(audio)
                print(f"You: {cityname}")
                get_weather(cityname)
            except:
                speak("Sorry, I couldn't understand the city name.")

    elif "hindi" in comm or "translate" in comm:
        speak("What do you want to translate?")
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
               to_translate = r.recognize_google(audio, language="hi-IN")
              
           
               result = translate_text(to_translate, dest_lang="en") 
               speak(f"The translation is: {result}")
            except:
                speak("Sorry, I couldn't understand what you said.")
    elif "exit" in comm:
        speak("Goodbye , Feel free to call me again whenever you need assistance.")
        exit()

    else:
        
        speak("Processing with AI...")
        ai_response = get_ai_response(comm)
        speak(ai_response)

if __name__ == "__main__":
    speak("Initializing Bug...")
    while True:
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("I'm Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            command = word.lower()
            print("You:",command )
            processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
