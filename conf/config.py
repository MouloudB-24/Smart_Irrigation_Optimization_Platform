import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load API KEY
load_dotenv()
API_KEY = os.environ["API_KEY"]

# Kafka
IoT_topic = "IoT_topic"
weather_topic = "weather_topic"

# Weather API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_PARAMS = {
    "q": "Nogent-sur-seine, FR",
    "appid": API_KEY,
    "units": "metric",
    "lang": "fr"
}