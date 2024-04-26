import pandas as pd 
import nsopw  
import name_combinations_split
import name_validation  
import db_res_insert
import db_name_combination_update
import subregistry_validation


def automation_start(config, df_input):
  print(config['selenium_states'])

  logger = config['logger']

  input_dob = df_input['SUBJ_DATE_OF_BIRTH']

  df_res_combination_check = pd.read_excel(config["res_combinations_check"])

  # raise ("manual error")
  df_input_names = name_combinations_split.input_combinations(df_input['Name_Combinations'])
  df_input_names['middlename'] = df_input['SUBJ_MIDDLE_NAME']   
  df_input_names['age'] = df_input['SUBJ_AGE']

  df_input_names = db_name_combination_update.db_name_insert(config, df_input_names, df_input['ID'])
  # print(df_input_names)
  # overall_hit_match = "clear"
  for i, input_row in df_input_names.iterrows():

    if not input_row['bot_status'] == 'completed':
      first_name = df_input_names['firstname'][i]
      last_name = df_input_names['lastname'][i]
      df_results = nsopw.nsopw_search(first_name, last_name)

      if not df_results.empty:
        hit_match, df_results = name_validation.name_matching(input_row, df_results, df_res_combination_check)

        if hit_match:
          df_results = subregistry_validation.navigation(df_results, config['bs_states'], config['selenium_states'], input_dob)
          hit_match = (df_results['HitStatus'] == 'Hit').any()
      else:
        hit_match = False

      df_results['name_combo_id'] = i+1
      df_results['name_combo'] = df_input_names['firstname'][i] +','+df_input_names['lastname'][i]

      if hit_match:
        input_row['hitstatus'] = 'Hit'
        df_input_names.at[i, 'hitstatus'] = "Hit"
        # print('df_input_names', df_input_names)
      else:
        input_row['hitstatus'] = 'Clear'
        df_input_names.at[i, 'hitstatus'] = "clear"
        
      
      input_row['bot_status'] = 'completed'

      db_res_insert.insert_res_row(config, df_results, df_input['ID'], input_row)

  hit_match = (df_input_names['hitstatus'] == 'Hit').any()
  if hit_match:
    hit_match  = 'Hit'
  else:
    hit_match = 'Clear'

  return hit_match


      
  
  
  



