import pandas as pd
import result_name_combinations

def name_split(name):
  last_name = name.split(",")[0]
  if len(name.split(",")[1].strip().split(" "))>1:
    first_name = name.split(",")[1].strip().split(" ")[0].strip()
    middle_name = name.split(",")[1].strip().split(" ")[1].strip()
  else:
    first_name = name.split(",")[1].strip()
    middle_name = ''
  return first_name, last_name, middle_name

def result_row_hit_check(df_result_row, df_input_row, df_res_combination_check):

      for i, row in df_result_row.iterrows():
            firstname = ""
            lastname = ""
            middlename = ""
            age = ""
            input_first_name = df_input_row['firstname'].strip()
            input_last_name = df_input_row['lastname'].strip()
            input_middle_name =  df_input_row['middlename'].strip()
            input_age =  df_input_row['age']

            if input_first_name.strip().lower() == row['firstname'].strip().lower():
                  df_result_row.at[i, 'firstname_match'] = "match"
                  firstname = "match"
            else:
                  df_result_row.at[i, 'firstname_match'] = "notmatch"
                  firstname = "notmatch"

            if input_last_name.strip().lower() == row['lastname'].strip().lower():
                  df_result_row.at[i, 'lastname_match'] = "match"
                  lastname = "match"
            else:
                  df_result_row.at[i, 'lastname_match'] = "notmatch"
                  lastname = "notmatch"
            
            if input_middle_name and row['middlename']:
                  if input_middle_name.lower().strip() == row['middlename'].lower().strip():
                        df_result_row.at[i, 'middlename_match'] = "match"
                        middlename = "match"
                  
                  elif input_middle_name.lower()[0].strip() == row['middlename'].lower()[0].strip():
                        df_result_row.at[i, 'middlename_match'] = "match"
                        middlename = "match"
                  else:
                        df_result_row.at[i, 'middlename_match'] = "notmatch"
                        middlename = "notmatch"
            else:
                  df_result_row.at[i, 'middlename_match'] = "notavailable"
                  middlename = "notavailable"

            if input_age and row['age']:
                  if  int(input_age) == int(row['age']):  
                        df_result_row.at[i, 'age_match']  = "match"     
                        age = "match" 
                  elif int(input_age) == int(row['age'])+1 or  int(input_age) == int(row['age'])-1:
                        df_result_row.at[i, 'age_match'] = "partial"
                        age = "partial"
                  else:
                        df_result_row.at[i, 'age_match']  = "notmatch" 
                        age = "notmatch"
            else:
                  df_result_row.at[i, 'age_match'] = "notavailable" 
                  age = "notavailable"

            filtered_df = df_res_combination_check[
                              (df_res_combination_check['firstname'] == firstname) &  # Filter by firstname
                              (df_res_combination_check['lastname'] == lastname) &     # Filter by lastname
                              (df_res_combination_check['middlename'] == middlename) &  # Filter by middlename
                              (df_res_combination_check['age'] == age)                # Filter by age
                                    ]
            filtered_df = filtered_df.reset_index(drop=True)
            df_result_row.at[i, "match"] = filtered_df["HitStatus"][0]
            
      print(df_result_row)
      # df_result_row.to_excel('df_result_row'+str(i)+'.xlsx')
      hit_match = (df_result_row['match'] == 'Hit').any()
      return hit_match

def name_matching(df_input_row, df_result, df_res_combination_check):
      for i, row in df_result.iterrows():
            name = row['Offender']
            status, df_result_name_combination = result_name_combinations.df_name_combinations(name)
            name_combination_error = False
            if not isinstance(row['Aliases'], float):
                  if not row['Aliases'] == '':
                        for name in row['Aliases'].split("\n"):
                              status, df_result_name_combination_alias = result_name_combinations.df_name_combinations(name)
                              if status == 'success':
                                    df_result_name_combination = pd.concat([df_result_name_combination, df_result_name_combination_alias], ignore_index=True)
                                    name_combination_error = False
                              else:

                                    name_combination_error = name
                                    break

            df_result_name_combination['age'] = row['Age']
            df_result_name_combination['firstname_match'] = ''
            df_result_name_combination['lastname_match'] = ''
            df_result_name_combination['middlename_match'] = ''
            df_result_name_combination['age_match'] = ''
            df_result_name_combination['match'] = ''
            
       
            if name_combination_error:
                 df_result.at[i, 'HitStatus'] = 'Manual'
                 df_result.at[i, 'comment'] = 'Name combination is failed in ='+ name_combination_error
                 
            else:
                  df_result_name_combination = df_result_name_combination.drop_duplicates()
                  hit_match = result_row_hit_check(df_result_name_combination, df_input_row, df_res_combination_check)
                  if hit_match:
                        df_result.at[i, 'HitStatus'] = 'Hit'
                  else:
                        df_result.at[i, 'HitStatus'] = 'Clear'

      hit_match = (df_result['HitStatus'] == 'Hit').any()
      return hit_match, df_result

if __name__ == '__main__':
      df_input = pd.read_excel("data.xlsx")
      df_results = pd.read_csv("output.csv")
      for i, row in df_input.iterrows():
            hit_match = name_matching(row, df_results)

            if hit_match:
                  df_input.at[i, 'result'] = 'Hit'
            else:
                  df_input.at[i, 'result'] = 'Clear'

      print(df_input)

      df_input.to_csv("output1.csv", index=False)
