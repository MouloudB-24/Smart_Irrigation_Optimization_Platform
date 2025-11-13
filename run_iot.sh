#!/usr/bin/bash

# Project folder
PROJECT_FOLDER="/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
cd $PROJECT_FOLDER

# Read global parameters
source .gps

# Input data
export INPUT_DATA_FILE="site.json"

# Data site
export SITE_IDS=1
export MAX_DOCS=5

# IoT topic
export IoT_TOPIC="iot_topic"

# Mongodb
export MONGO_COLLECTION="sensor_data"

# venv
source venv/bin/activate

# run
python3 -m data_ingestion.app_iot.main_iot
