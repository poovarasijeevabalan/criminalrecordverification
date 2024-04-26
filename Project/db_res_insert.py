import mysql.connector
import pandas as pd
import z_mysql_connect


def insert_res_row(config, df_results, record_id, input_row):
  # Establish connection to the MySQL database
  cnx = z_mysql_connect.connection(config)
  cursor = cnx.cursor()
  query = f"update automation.tbl_name_combo set hitstatus = '{input_row['hitstatus']}', bot_status = '{input_row['bot_status']}' where Id = {input_row['Id']}"
  cursor.execute(query)
  # Commit the transaction
  cnx.commit()
  print(df_results)
  for i, row in df_results.iterrows():
      # print("""INSERT INTO `automation`.`tbl_res_nsopw`
      #           (`record_id` ,`name_id`, `name_combo`, `Offender`,`Age`,`Aliases`,`Address`, `state_code`,`link`, `sub_reg_dob`,`Hit_status`,  `comment`)
      #           VALUES
      #           ({record_id},'{input_row['Id']}','{row['name_combo']}','{row['Offender']}','{row['Age']}','{row['Aliases']}','{row['Address']}', '{row['state_code']}','{row['Link_url']}', '{row['sub_reg_dob']}','{row['HitStatus']}','{row['comments']}');
      #           """)
      query = f"""INSERT INTO `automation`.`tbl_res_nsopw`
                (`record_id` ,`name_id`, `name_combo`, `Offender`,`Age`,`Aliases`,`Address`, `state_code`,`link`, `sub_reg_dob`,`Hit_status`,  `comment`)
                VALUES
                ({record_id},'{input_row['Id']}','{row['name_combo']}','{row['Offender']}','{row['Age']}','{row['Aliases']}','{row['Address']}', '{row['state_code']}','{row['Link_url']}', '{row['sub_reg_dob']}','{row['HitStatus']}','{row['comments']}');
                """
      
      cursor.execute(query)
      cnx.commit()
  cursor.close()
  cnx.close() 

if __name__ == '__main__':
  df_results = pd.read_excel("df_res.xlsx")
  record_id = 2
  insert_res_row(df_results, record_id)