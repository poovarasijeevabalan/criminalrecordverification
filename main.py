# import system libraries
import os
import json
import sys
import time
import traceback
import platform
import getpass

# Framework library imports
from Project.z_log_messages_json import perform_logging
from Project.z_init_application import init_all_application
from Project.z_init_settings import init_all_settings
from Project.z_get_transaction_item import get_item
from Project.z_set_transaction_status import update_status
from Project.z_process import process

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)

# Get the full path to the config.json and properties file
config_path = "config.json"


if not getattr(sys, "frozen", False):
    # not running from an executable (e.g., PyInstaller bundle)
    config_path = os.path.join(current_path, config_path)

# Read properties
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
logger.info(config["process_name"] + "-- execution started")
config["logger"] = logger


# Framework
class Framework:
    """Represents the automation framework."""

    def __init__(self, config):
        self.config = config
        logger.debug("Framework initiated")

    def init_all_settings(self):
        """initiate all applications"""
        self.config = init_all_settings(self.config)
        logger.debug("init all settings completed")

    def init_all_applications(self):
        """reading input excel to process queue"""
        self.config = init_all_application(self.config)
        logger.debug("init all application completed")

    def get_transaction_data(self):
        """getting transaction data for processing the order"""
        dict_transaction = {}
        self.dict_transaction = get_item(self.config, dict_transaction)
        self.dict_transaction["retry count"] = 0
        logger.debug("get transaction data completed")

    def process_transaction(self):
        """processing the order"""
        logger.info("process started")
        try:
            self.dict_transaction["bot_status"] = ""
            self.dict_transaction = process(self.config, self.dict_transaction)
            if not self.dict_transaction["bot_status"]:
                self.dict_transaction["bot_status"] = "completed"
            logger.debug("process completed")

        except Exception as e:
            logger.error(traceback.format_exc())
            self.dict_transaction["bot_status"] = "error"
            self.dict_transaction["bot_comments"] = str(e).replace("'", "")

    def set_transaction_status(self):
        """update the status of the process transaction"""
        update_status(self.config, self.dict_transaction)
        logger.debug("set transaction completed")

    def run(self):
        self.init_all_settings()
        self.init_all_applications()
        while True:
            self.get_transaction_data()  # call get transaction data

            if self.dict_transaction["is_transaction_empty"]:
                """checking if the transaction data is empty"""
                logger.debug("transaction data received empty. so exiting the process")
                time.sleep(3)
                continue

            """ transaction item is not empty, so proceed to process further"""
            self.dict_transaction["retry count"] = 1
            while True:
                self.process_transaction()  # call process transaction
                self.set_transaction_status()  # call set transaction status

                # below logic is for system exception retry count
                if self.dict_transaction["bot_status"] == "error":
                    if (
                        self.dict_transaction["retry count"]
                        < self.config["max_retry_count"]
                    ):
                        self.dict_transaction["retry count"] = (
                            self.dict_transaction["retry count"] + 1
                        )
                        continue
                    else:
                        break
                break


framework = Framework(config)
framework.run()
