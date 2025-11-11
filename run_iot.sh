#!/usr/bin/bash

source /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/.gps

export INPUT_DATA_FILE="beauce.json"

# Data site
export SITE_IDS=1
export MAX_DOCS=12

# IoT topic
export IoT_TOPIC="IoT_TOPIC"

# Mongodb
export MONGO_COLLECTION="sensor_data"

# venv
source /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/venv/bin/activate

# run
python3 /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/main_iot.py
