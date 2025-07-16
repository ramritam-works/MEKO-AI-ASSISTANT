import os
from kivy.config import Config

width, height = 1920,1080 

Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'fullscreen', 'True')

IP_ADDR_API_URL = os.environ.get("IP_ADDR_API_URL")
NEWS_FETCH_API_URL = os.environ.get("NEWS_FETCH_API_URL")
NEWS_FETCH_API_KEY = os.environ.get("NEWS_FETCH_API_KEY")
WEATHER_FORCAST_API_URL = os.environ.get("WEATHER_FORCAST_API_URL")
WEATHER_FORCAST_API_KEY = os.environ.get("WEATHER_FORCAST_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SCREEN_WIDTH = Config.getint('graphics', 'width')
SCREEN_HEIGHT = Config.getint('graphics', 'height')