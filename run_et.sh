#!/usr/bin/bash

# Project folder
PROJECT_FOLDER="/home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform"
cd $PROJECT_FOLDER

# Read global parameters
source .gps

# Mongodb
export MONGO_COLLECTION="evapotranspiration_data"

# API 
export BBOX_COORDS="1.240,48.320,-1.150,48.380"
export START_DATE="2025-06-01"
export END_DATE="2025-06-05"

#  Topic
export ET_TOPIC="evapotrans_topic"

# Docs
export MAX_DOCS=1

# venv
source venv/bin/activate

# run
python3 -m data_ingestion.app_satellite.earth_engine_api.main_evapotranspiration


# 


