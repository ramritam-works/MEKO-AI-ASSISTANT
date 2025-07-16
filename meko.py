import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import sys
import pyautogui
import subprocess as sp
import webbrowser
import imdb
from kivy.uix import widget,image,label,boxlayout,textinput
from kivy import clock
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GEMINI_API_KEY
from utils import speak, youtube, search_on_google, search_on_wikipedia, get_news, weather_forecast, find_my_ip
from meko_button import MekoButton
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

class Meko(widget.Widget):
    def __init__(self, **kwargs):
        super(Meko, self).__init__(**kwargs)
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]
        self.volume_history_size = 140

        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        
        self.add_widget(image.Image(source='static/border.eps.png',size=(1920,1080)))
        self.circle = MekoButton(size=(284.0,284.0),background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(source='static/meko.gif', size=(self.max_size, self.max_size), pos=(SCREEN_WIDTH / 2 - self.max_size / 2, SCREEN_HEIGHT / 2 - self.max_size / 2)))

        time_layout = boxlayout.BoxLayout(orientation='vertical',pos=(150,900))
        self.time_label = label.Label(text='', font_size=24, markup=True,font_name='static/mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)

        clock.Clock.schedule_interval(self.update_time, 1)

        self.title = label.Label(text='[b][color=3333ff]MEKO A VIRTUAL ASSISTANT[/color][/b]',font_size = 42,markup=True,font_name='static/dusri.ttf',pos=(920,900))
        self.add_widget(self.title)
        
        self.subtitles_input = textinput.TextInput(
            text='Hey Ramritam! I am your personal assistant',
            font_size=24,
            readonly=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=80,
            pos=(700, 100),
            width=1200,
            font_name='static/teesri.otf',
        )
        self.add_widget(self.subtitles_input)

        self.vrh=label.Label(text='',font_size=30,markup=True,font_name='static/mw.ttf',pos=(1300,500))
        self.add_widget(self.vrh)

        self.vlh=label.Label(text='',font_size=30,markup=True,font_name='static/mw.ttf',pos=(400,500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        keyboard.add_hotkey('`',self.start_recording)

    def take_command(self):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print("Recognizing....")
                queri = r.recognize_google(audio, language='en-in')
                return queri.lower()

            except Exception:
                speak("Sorry I couldn't understand. Can you please repeat that?")
                queri = 'None'

    def start_recording(self, *args):
            print("recording started") 
            threading.Thread(target=self.run_speech_recognition).start()
            print("recording ended") 


    def run_speech_recognition(self):
            print('before speech rec obj')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source) 
                print("audio recorded")
                
            print("after speech rec obj") 
            
            try:
                query=r.recognize_google(audio,language="en-in") 
                print(f'Recognised: {query}')
                clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input,'text',query))
                self.handle_meko_commands(query.lower())
                                
            except sr.UnknownValueError:
                print("Google speech recognition could not understand audio")
                
            except sr.RequestError as e:
                print(e) 
            return query.lower()  
        
    def update_time(self,dt):
            current_time = time.strftime('TIME\n\t%H:%M:%S')
            self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'

    def update_circle(self, dt):
            try:
                self.size_value = int(np.mean(self.volume_history))
                
            except Exception as e:
                self.size_value = self.min_size
                print('Warning:',e)
                
            if self.size_value <= self.min_size:
                self.size_value = self.min_size
            elif self.size_value >= self.max_size:
                self.size_value = self.max_size                                     
            self.circle.size = (self.size_value,self.size_value)
            self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)

    def update_volume(self,indata,frames,time,status):
            volume_norm = np.linalg.norm(indata) * 200
            self.volume = volume_norm
            self.volume_history.append(volume_norm)
            self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''
                
            self.vrh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''  
                
            if len(self.volume_history) > self.volume_history_size:
                self.volume_history.pop(0)  

    def start_listening(self):
            self.stream = sd.InputStream(callback=self.update_volume) 
            self.stream.start()

    def get_gemini_response(self,query):
        try:
            response = model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I'm sorry, I couldn't process that request."
            
    def handle_meko_commands(self,query):  
            try:
                if "how are you" in query:
                    speak("I am absolutely fine sir. What about you")

                elif "open command prompt" in query:
                    speak("Opening command prompt")
                    os.system('start cmd')

                elif "open camera" in query:
                    speak("Opening camera for you sir")
                    sp.run('start microsoft.windows.camera:', shell=True)

                elif "open notepad" in query:
                    speak("Opening notepad for you sir")
                    notepad_path = "C:\\Users\\ACER\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                    os.startfile(notepad_path)

                elif "open paint" in query:
                    speak("Opening paint for you sir")
                    paint_path = "C:\\Users\\ACER\\AppData\\Local\\Microsoft\\WindowsApps\\mspaint.exe"
                    os.startfile(paint_path)

                elif 'ip address' in query:
                    ip_address = find_my_ip()
                    speak(
                        f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    print(f'Your IP Address is {ip_address}')

                elif "youtube" in query:
                    speak("What do you want to play on youtube sir?")
                    video = self.take_command().lower()
                    youtube(video)

                elif "search on google" in query:
                    speak(f"What do you want to search on google sir?")
                    query = self.take_command().lower()
                    search_on_google(query)

                elif "search on wikipedia" in query:
                    speak("what do you want to search on wikipedia sir?")
                    search = self.take_command().lower()
                    results = search_on_wikipedia(search)
                    speak(f"According to wikipedia,{results}")

                elif 'weather' in query:
                    ip_address = find_my_ip()
                    speak("tell me the name of your city")
                    query = self.take_command().lower()
                    city = query
                    speak(f"Getting weather report for your city {city}")
                    weather, temp, feels_like = weather_forecast(city)
                    speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

                elif "movie" in query:
                    movies_db = imdb.IMDb()
                    speak("Please tell me the movie name:")
                    text = self.take_command()
                    movies = movies_db.search_movie(text)
                    speak("searching for" + text)
                    speak("I found these")
                    for movie in movies:
                        title = movie["title"]
                        year = movie["year"]
                        speak(f"{title}-{year}")
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info["rating"]
                        cast = movie_info["cast"]
                        actor = cast[0:5]
                        plot = movie_info.get('plot outline', 'plot summary not available')
                        speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                            f"The plot summary of movie is {plot}")

                        print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                            f"The plot summary of movie is {plot}")
                        
                else:
                    gemini_response = self.get_gemini_response(query)
                    gemini_response = gemini_response.replace("*","")
                    if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                        speak(gemini_response)
                        print(gemini_response)
                
            except Exception as e:
                print(e)