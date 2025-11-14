#!/usr/bin/bash

# Project folder
PROJECT_FOLDER="/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
cd $PROJECT_FOLDER

# Read global parameters
source .gps

# Mongodb
export MONGO_COLLECTION="air_temperature"

# API Copernicus
export LATITUDE=48.350
export LONGITUDE=-1.195

#  Topic
export ST_TEMP_TOPIC="air_temp_topic"

# Max docs
export MAX_DOCS=1

# Venv
source venv/bin/activate

# run
python3 -m data_ingestion.app_satellite.nasa_power_api.main_air_temperature



