# System libraries
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import time
import traceback
import process_start

def process(config, dict_transaction):
    """build all business process code here"""

    
    logger =config['logger']

    dict_trans_item = dict_transaction['dict_trans_item']

    logger.info(str(dict_trans_item['ID'])+" - transaction started")

    
    dict_transaction['hit_match'] = process_start.automation_start(config, dict_trans_item)

    logger.info(str(dict_trans_item['ID'])+" - transaction completed")
    
    return dict_transaction
