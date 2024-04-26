# system libraries
import os
import sys
import json
import pandas as pd
import traceback
import platform
import getpass
import pytest

# project libraries
from Project.z_log_messages_json import perform_logging
from Project.z_init_application import init_all_application
from Project.z_process import process

# testing
from Test import autotest

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

# Get the full path to the config.json and properties file
config_path = "config.json"
with open(config_path) as f:
    config = json.load(f)

# assign current path to config
config["current_path"] = current_path

# bot id
machine_id = platform.node()
user_name = getpass.getuser()
config["bot_id"] = f"{machine_id}-{user_name}"

# logger initiations
logger = perform_logging(config)
config["logger"] = logger
logger.info(config["process_name"] + "-- execution started")

config = init_all_application(config)

dict_transaction = {}
# dict_transaction['df_ddqc_report'] = pd.read_excel(r"C:\Users\mjeevaba\Documents\Python\DDQC\DDQC 2.0\Sharepath\queue\input file3.xlsx", skiprows=3)

input_path = r"C:\Users\mjeevaba\Documents\Python\DDQC\DDQC 2.0\Sharepath\Phase 3 Expected Result.xlsx"

dict_transaction["df_ddqc_report"] = pd.read_excel(input_path)

try:
    dict_transaction = process(config, dict_transaction)
except Exception as e:
    logger.error(traceback.format_exc())


# autotest.auto_testing(config, dict_transaction)
