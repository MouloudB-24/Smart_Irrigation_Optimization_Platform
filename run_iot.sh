#!/usr/bin/bash

# Level debug definition:
# 0 Debug       -> Allot of information will be printed, including printing site configuration to logfile.
# 1 Info        -> We just printing that processes is starting/ending
# 2 Warning     -> Will decide
# 3 Error       -> used in any try/except block
# 4 Critical    -> used when we going to kill the programm

# Console Handler
export CONSOLE_DEBUG_LEVEL=1

# FILE Handler
export FILE_DEBUG_LEVEL=0

# Data
export LOGGING_FILE="logger_IoT"
export INPUT_DATA_FILE="beauce.json"


# Data site
export SITE_IDS=101
export NB_SONSORS=12

# venv
source /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/venv/bin/activate

# Start program
python3 /home/mouloud/Documents/projects/Smart_Irrigation_Optimization_Platform/main.py
