import speech_recognition as sr
import pyttsx3
from datetime import datetime, date
import wikipedia
import requests
import time

def speak(text):
    robot_mouth.say(text)
    robot_mouth.runAndWait()

# Initialize recognizer and TTS engine
robot_ear = sr.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain = ""

# Set up pyttsx3 to use an English voice
voices = robot_mouth.getProperty('voices')
for voice in voices:
    if 'en' in voice.id or 'english' in voice.name.lower():
        robot_mouth.setProperty('voice', voice.id)
        break

# Function to get weather information
def get_weather(city):
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    if not city:
        return "Please provide a city name."
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        content = f"""
        Current temperature is {current_temperature} degrees Celsius.
        Air pressure is {current_pressure} hPa.
        Humidity is {current_humidity}%.
        Today's weather is {weather_description}.
        """
        speak(content)
        time.sleep(20)
        return "I am listening"
    else:
        return "City not found."

while True:  # Continuous interaction loop
    with sr.Microphone() as mic:
        print("Robot: I'm listening")
        speak("I'm listening")
        audio = robot_ear.listen(mic)

    print("Robot:...")

    try:
        you = robot_ear.recognize_google(audio)
        print("You said:", you)
    except sr.UnknownValueError:
        you = ""
    except sr.RequestError:
        robot_brain = "Sorry, the service is not available"
        print("Robot:", robot_brain)
        speak(robot_brain)
        continue

    if you == "":
        robot_brain = "I didn't catch that, please try again"
    elif "hello" in you.lower():
        robot_brain = "Hello, I am Python"
    elif "today" in you.lower():
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    elif "time" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H hours %M minutes %S seconds")
    elif "goodbye" in you.lower():
        robot_brain = "Goodbye"
        print("Robot:", robot_brain)
        speak(robot_brain)
        break
    elif "weather" in you.lower():
        words = you.lower().split()
        if len(words) > 2:
            city = ' '.join(words[2:])  # Assuming the format "weather <city>"
            robot_brain = get_weather(city)
        else:
            robot_brain = "Please say the city name after the word 'weather'."
    else:
        try:
            # Search Wikipedia for the spoken query
            robot_brain = wikipedia.summary(you, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            robot_brain = "There are multiple entries for this topic. Please be more specific."
        except wikipedia.exceptions.PageError:
            robot_brain = "I couldn't find information about this topic."

    print("Robot:", robot_brain)
    speak(robot_brain)
