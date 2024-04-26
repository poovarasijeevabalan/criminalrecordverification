import pandas as pd
import os, sys
import json
import shutil


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from z_init_application import init_all_application
import z_mysql_connect


def get_item(config, dict_transaction):
    """get transaction item from db queue"""

    # connection to mysql
    cnx = z_mysql_connect.connection(config)
    cursor = cnx.cursor()

    # Query to fetch the inserted row

    select_query = f"SELECT * FROM nsopw_table WHERE Web_Bot_Status='in-progress' and Web_Bot_ID = '{config['bot_id']}' limit 1"
    cursor.execute(select_query)
    rows = cursor.fetchall()  
    if not rows:
        select_query = f"SELECT * FROM nsopw_table WHERE Web_Bot_Status='system exception' and Web_Rerun_Count<3 and Web_Bot_ID = '{config['bot_id']}' limit 1"
        cursor.execute(select_query)
        rows = cursor.fetchall()  # Fetch all rows
    if not rows:
        select_query = f"SELECT * FROM nsopw_table WHERE Web_Bot_Status='yet to start1'  and ID = 104 limit 1"
        # select_query = f"SELECT * FROM nsopw_table WHERE  Web_Bot_Status='system exception' LIMIT 1;"
        cursor.execute(select_query)
        rows = cursor.fetchall() 

    dict_transaction["is_transaction_empty"] = False
    if not rows:
        dict_transaction["is_transaction_empty"] = True
    

    if not dict_transaction["is_transaction_empty"]:
        column_names = [i[0] for i in cursor.description]
        df_trans_tbl = pd.DataFrame(rows, columns=column_names)


        dict_trans_item = {}
        for i, row in df_trans_tbl.iterrows():
            
            dict_trans_item["idx"] = i
            for col in df_trans_tbl.columns:
                dict_trans_item[col] = row[col]
            break

        if not dict_transaction["is_transaction_empty"]:
            id = rows[0][0]
            query = f"Update nsopw_table set Web_Bot_Status='in-progress', Web_Started_Date=now(), Web_Bot_ID='{config['bot_id']}' where id={id}"
            cursor.execute(query)
            cnx.commit()
        
        dict_transaction["dict_trans_item"] = dict_trans_item
    
    cursor.close()
    cnx.close()

    dict_transaction['hit_match'] = ''
    return dict_transaction


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)


