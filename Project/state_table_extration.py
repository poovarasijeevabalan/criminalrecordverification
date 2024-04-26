import pandas as pd
from WebAutomationActivities import Activity
from selenium.webdriver.common.by import By

def States_infor():
    activity = Activity("Chrome", maximize=True)
    driver = activity.browser()
    activity.url_navigate("https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=53971", delay_after=2)

    df_result_states= pd.DataFrame()  # Initialize df_results here

    # table_text_states = activity.get_text(xpath="//table[@id='nsopwdt']", delay_after=10)
    df_result_state = activity.get_html_table(xpath="//table[@class='table table-bordered responsive-utilities table-hover table-condensed mrgn-bttm-0']", delay_after=10)
    # df_result_states = pd.concat([df_result_state, df_result_states], ignore_index=True)

    df_result_state.to_csv('All_States_code.csv', index=True)
    driver.quit()
    return df_result_state


if __name__ =="__main__":
  States_infor()
    