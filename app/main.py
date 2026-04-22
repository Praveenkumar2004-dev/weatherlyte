from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# 🔐 Load .env
load_dotenv()

app = FastAPI()

# 🔥 CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for your project)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 API KEY
API_KEY = os.getenv("WEATHER_API_KEY")


@app.get("/")
def home():
    return {"message": "Weather API is running 🚀"}


@app.get("/weather/{city}")
def get_weather(city: str):

    # 🧠 Clean city input
    city = city.strip().title()

    # 🌍 API call
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # ❌ Error handling
    if response.status_code != 200 or "main" not in data:
        return {"error": "City not found"}

    # ✅ Response
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "timezone": data["timezone"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"]
    }