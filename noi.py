import speech_recognition as sr
from gtts import gTTS
from datetime import datetime, date
import wikipedia
import requests
import locale
import time
import webbrowser
import os
import playsound

def speak(text):
    tts = gTTS(text=text, lang='vi')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename, True)
    os.remove(filename)  # Clean up the audio file after playing    

# Initialize recognizer and TTS engine
robot_ear = sr.Recognizer()
robot_brain = ""
locale.setlocale(locale.LC_ALL, 'en_US.utf8')
wikipedia.set_lang("vi")  # Set Wikipedia language to Vietnamese

# Function to get weather information
def get_weather(city):
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    if not city:
        return "Vui lòng cung cấp tên thành phố."
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(
            day=now.day, month=now.month, year=now.year, 
            hourrise=sunrise.hour, minrise=sunrise.minute, 
            hourset=sunset.hour, minset=sunset.minute, 
            temp=current_temperature, pressure=current_pressure, humidity=current_humidity)
        speak(content)
        time.sleep(3)
        return "Tôi đang lắng nghe"
    else:
        return "Không tìm thấy địa chỉ của bạn"

while True:  # Continuous interaction loop
    with sr.Microphone() as mic:
        print("Robot: Tôi đang lắng nghe")
        speak("Tôi đang lắng nghe")
        audio = robot_ear.listen(mic)

    print("Robot:...")

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
        print("Bạn nói:", you)
    except sr.UnknownValueError:
        you = ""
    except sr.RequestError:
        robot_brain = "Xin lỗi, dịch vụ không hoạt động"
        print("Robot:", robot_brain)
        speak(robot_brain)
        continue

    if you == "":
        robot_brain = "Tôi không nghe rõ, vui lòng thử lại"
    elif "xin chào" in you.lower():
        robot_brain = "Xin chào, tôi là Python"
    elif "hôm nay" in you.lower():
        today = date.today()
        robot_brain = today.strftime("%B %d, %Y")
    elif "giờ" in you.lower():
        now = datetime.now()
        robot_brain = now.strftime("%H giờ %M phút %S giây")
    elif "mở bài" in you.lower():  # Changed trigger phrase to "mở bài"
        try:
            # Extract the song title from the user command
            query = you.lower().split("mở bài")[1].strip()
            # Construct the YouTube search URL
            youtube_url = f"https://www.youtube.com/results?search_query={query}"
            # Open the URL in a web browser
            webbrowser.open(youtube_url)
            robot_brain = f"Mở YouTube và tìm kiếm '{query}'"
        except IndexError:
            robot_brain = "Xin lỗi, tôi không nghe rõ bạn muốn tìm bài gì trên YouTube."
    elif "tạm biệt" in you.lower():
        robot_brain = "Tạm biệt"
        print("Robot:", robot_brain)
        speak(robot_brain)
        break
    elif "nhiệt độ"  in you.lower():
        words = you.lower().split()
        if len(words) > 2:
            city = ' '.join(words[2:])  # Assuming the format "nhiệt độ <city>"
            robot_brain = get_weather(city)
        else:
            robot_brain = "Vui lòng nói tên thành phố sau từ 'nhiệt độ'."
    else:
        try:
            # Search Wikipedia for the spoken query
            robot_brain = wikipedia.summary(you, sentences=1)
        except wikipedia.exceptions.DisambiguationError as e:
            robot_brain = "Có nhiều mục nhập cho chủ đề này. Vui lòng cụ thể hơn."
        except wikipedia.exceptions.PageError:
            robot_brain = "Tôi không tìm thấy thông tin về chủ đề này."

    print("Robot:", robot_brain)
    speak(robot_brain)
