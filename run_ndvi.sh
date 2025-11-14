#!/usr/bin/bash

# Project folder
PROJECT_FOLDER="/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
cd $PROJECT_FOLDER

# Read global parameters
source .gps

# Mongodb
export MONGO_COLLECTION="ndvi_data"

# API 
export BBOX_COORDS=-"1.240,48.320,-1.150,48.380"
# export TIME_INTERVAL="2025-11-01,2025-11-05"

#  Topic
export NDVI_TOPIC="ndvi_topic"

# Docs
export MAX_DOCS=1

# venv
source venv/bin/activate

# run
python3 -m data_ingestion.app_satellite.copernicus_api.main_ndvi

