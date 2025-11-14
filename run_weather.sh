#!/usr/bin/bash

# Project folder
PROJECT_FOLDER="/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
cd $PROJECT_FOLDER

# Read global parameters
source .gps


# Mongodb
export MONGO_COLLECTION="weather_data"

# API
export WEATHER_URL="https://api.openweathermap.org/data/2.5/weather"

# Topic
export WEATHER_TOPIC="weather_topic"

# Docs
export MAX_DOCS=1

# Venv
source venv/bin/activate

# run
python3 -m data_ingestion.app_weather.main_weather
