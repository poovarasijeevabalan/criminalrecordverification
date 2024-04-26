import logging
import datetime
import json

import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


def perform_logging(config):
    
    if not getattr(sys, 'frozen', False):
        # not running from an executable (e.g., PyInstaller bundle)
        log_directory = os.path.join(config["current_path"], config["log_path"])
    else:
        log_directory = config["log_path"]
    # Create the logger
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

        # Create the log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create a file handler
    filename = os.path.join(log_directory, f"{config['bot_id']} - log_{datetime.datetime.today().strftime('%Y-%m-%d')}.log")
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)

    # Define the custom JSON formatter
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'timestamp': timestamp,
                'level': record.levelname,
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'message': record.getMessage(),
                'process':config['process_name'],
            }
            return json.dumps(data)

    # Set the formatter to the custom JSON formatter
    formatter = JSONFormatter()
    file_handler.setFormatter(formatter)

    # Define the custom terminal formatter
    class TerminalFormatter(logging.Formatter):
        def format(self, record):
            timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            return f"{timestamp} | {record.levelname} | {record.module} | Line {record.lineno} | {record.getMessage()}"

    # Set the formatter to the custom terminal formatter
    terminal_formatter = TerminalFormatter()

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(terminal_formatter)
    # stream_handler.setFormatter(logging.Formatter('%(message)s'))

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Set the logger level based on the config
    log_level = config.get("log_level", "debug").upper()
    logger.setLevel(getattr(logging, log_level))

    return logger
