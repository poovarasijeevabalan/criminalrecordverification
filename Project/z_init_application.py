
import json
import pandas as pd
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import z_mysql_connect


def init_all_application(config):
    """Initiate all required application here for this project"""
   


    return config

if __name__=="__main__":
    with open("config.json") as f:
        config = json.load(f)
    config = init_all_application(config)
    Refs = config['Refs']
    