import mysql.connector
import pandas as pd
import z_mysql_connect


def db_name_insert(config, name_combinations, record_id):
  # Establish connection to the MySQL database
  connection = z_mysql_connect.connection(config)
  cursor = connection.cursor()

  cursor = connection.cursor()
  query = f"SELECT * FROM tbl_name_combo WHERE record_id = {record_id} "
  # query = f"SELECT * FROM tbl_name_combo WHERE record_id = 16 "
  cursor.execute(query)
  rows = cursor.fetchall()  # Fetch all rows
  column_names = [i[0] for i in cursor.description]
  df = pd.DataFrame(rows, columns = column_names)

  if not len(df) > 0:
     
    for i, row in name_combinations.iterrows():
        query = f"""INSERT INTO `automation`.`tbl_name_combo`
                  (`record_id`,`firstname`, `lastname`, `middlename`,`age`)
                  VALUES
                  ({record_id},'{row['firstname']}','{row['lastname']}','{row['middlename']}','{row['age']}');
                  """
        # Execute the query
        cursor.execute(query)
        # Commit the transaction
        connection.commit()

    query = f"SELECT * FROM tbl_name_combo WHERE record_id = {record_id} "
    cursor.execute(query)
    rows = cursor.fetchall()  # Fetch all rows
    column_names = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns = column_names)
  print(df)
  # Close cursor and connection
  cursor.close()
  connection.close() 
  return df

if __name__ == '__main__':
  name_combinations= pd.DataFrame({
        'firstname': ['John', 'Jane', 'Robert'],
        'lastname': ['Doe', 'Smith', 'Johnson'],
        'middlename': ['Michael', 'Ann', 'Lee'],
        'age': [35, 28, 42]
    })
  record_id = 1
  db_name_insert(name_combinations, record_id)