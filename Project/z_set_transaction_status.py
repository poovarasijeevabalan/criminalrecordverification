import pandas as pd
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
import z_mysql_connect


def update_status(config, dict_transaction):
    """update transaction status to the respective queue item"""
    # Define the values to be updated
    id = dict_transaction["dict_trans_item"]["ID"]
    Record_Status = dict_transaction['hit_match']

    if dict_transaction["bot_status"] == "completed":
        # success
        update_query = f"update nsopw_table set Web_Bot_Status = 'completed', Web_Comments = '',Record_Status='{Record_Status}', Web_Bot_ID='{config['bot_id']}',Web_Completed_Date=now() where id='{id}';"

    elif dict_transaction["bot_status"] == "business exception":
        # Business exception
        update_query = f"update nsopw_table set Web_Bot_Status = 'business exception', Web_Comments = '{dict_transaction['bot_comments']}', Web_Bot_ID='{config['bot_id']}',Web_Completed_Date=now() where id='{id}';"

    else:
        # System exception
        update_query = f"update nsopw_table set Web_Bot_Status = 'system exception', Web_Rerun_Count='{dict_transaction['retry count']}', Web_Comments = '{dict_transaction['bot_comments']}', Web_Bot_ID='{config['bot_id']}',Web_Completed_Date=now() where id='{id}';"

    print(update_query)

    cnx = z_mysql_connect.connection(config)
    cursor = cnx.cursor()

    # Execute the insert query
    cursor.execute(update_query)

    # Commit changes and close cursor and connection
    cnx.commit()

    # transaction duration
    trans_duration_query = f"UPDATE nsopw_table SET Web_Transaction_Duration = TIMEDIFF(Web_Completed_Date, Web_Started_Date) where id = {id};"

    # Execute the insert query
    cursor.execute(trans_duration_query)

    # Commit changes and close cursor and connection
    cnx.commit()

    cursor.close()
    cnx.close()

    return config
