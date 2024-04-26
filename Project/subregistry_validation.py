import nsopw
import  Dob_Bs
import DOB_s
import pandas as pd
import Dob_match

def navigation(df_results, bs_list, selenium_list, input_dob):
  bs_list = bs_list.split(",")
  selenium_list = selenium_list.split(",")
  print(selenium_list)
  for i, row in df_results.iterrows():
    dob = None 
    if not row['HitStatus'] == 'Clear':

      try:
        state_code = row['state_code']
        link_url = row['Link_url']

        if state_code in bs_list:
          dob = Dob_Bs.DOB_Extraction(link_url)
          df_results.at[i, 'sub_reg_dob'] = dob
          print(link_url, dob)
        
        elif state_code in selenium_list:
          dob = DOB_s.DOB_Extraction(link_url, state_code)
          df_results.at[i, 'sub_reg_dob'] = dob
          print(link_url, dob)
      except:
        df_results.at[i, 'HitStatus'] = "Error"
        df_results.at[i, 'comment'] = "error during extraction"
        
    if dob:
      if dob == "NA" or dob == "Error":
        df_results.at[i, 'HitStatus'] = "Manual"
      else:
        dob_status = Dob_match.dob_match(input_dob, dob)
        if not(dob_status == "match" or dob_status == "partial"):
          df_results.at[i, 'HitStatus'] = "Clear"
          print("date not matched")

  return df_results



if __name__ == '__main__':
  first_name = "john"  # Replace with the desired first name
  last_name = "doe"    # Replace with the desired last name
  df_results = nsopw.nsopw_search(first_name, last_name)

  bs_list = ['MI']
  selenium_list = ['CA']

  df_results = navigation(df_results, bs_list, selenium_list)
  df_results.to_csv('state_validation.csv', index = True)
  print(df_results)
