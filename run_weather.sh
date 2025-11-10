#!/usr/bin/bash

source .gps

# Mongodb
export MONGO_COLLECTION="weather_data"

# API
export BASE_URL="https://api.openweathermap.org/data/2.5/weather"

# Topic
export WEATHER_TOPIC="Weather_topic"

# run
python3 /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/main_weather.py
