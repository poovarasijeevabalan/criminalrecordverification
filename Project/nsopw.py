import pandas as pd
from WebAutomationActivities import Activity
from selenium.webdriver.common.by import By
import state_code_extract


def nsopw_search(first_name, last_name):
    activity = Activity("Chrome", maximize=True)
    driver = activity.browser()
    activity.url_navigate("https://www.nsopw.gov/", delay_after=2)

    bool_search = activity.element_exist(xpath="//input[@id='firstname']", timeout=5)
    if bool_search:
        activity.sendkeys(xpath="//input[@id='firstname']", str_value=first_name.strip())
        activity.sendkeys(xpath="//input[@id='lastname']", str_value=last_name.strip())
        activity.click(xpath="//button[@id='searchbyname']", delay_after=2)

        bool_disclaimer = activity.element_exist(xpath="//a[contains(text(),'NSOPW Conditions of')]", timeout=5)
        if bool_disclaimer:
            print("disclaimer")
            activity.click(xpath="//button[@id='confirmBtn']", delay_after=5)
            print(driver.title)
        else:
            print("no disclaimer")
  
    next_button = activity.element_exist(xpath="//a[@id='nsopwdt_next']", timeout= 10)
    if next_button:
        bool_All_entitites = activity.element_exist(xpath="//select[@name='nsopwdt_length']", timeout=5)
        if bool_All_entitites:
            activity.click(xpath="//select[@name='nsopwdt_length']")
            activity.click(xpath="//option[text()='All' and @value='-1']", delay_after=5)
        else:
            print("no")
    df_results = pd.DataFrame()  # Initialize df_results here

    table_text = activity.get_text(xpath="//table[@id='nsopwdt']", delay_after=10)
    if 'No data available in table' in table_text:
        print(table_text)
    else:
        df_result = activity.get_html_table(xpath="//table[@id='nsopwdt']", delay_after=10)
        df_results = pd.concat([df_results, df_result], ignore_index=True)
    
        get_links = driver.find_elements(By.XPATH, "//a[@class='ext']")
        links = []
        for link in get_links:
            link_url = link.get_attribute("href")
            links.append(link_url)
        df_results['Link_url'] = links


    df_results['HitStatus'] = ''
    df_results['comments'] = ''
    df_results['state_code'] = ''
    df_results['sub_reg_dob'] = ''

    for i, row in df_results.iterrows():
        address = row['Address']
        state_code = state_code_extract.state_code_extr(address)
        df_results.at[i, 'state_code'] = state_code

    df_results.to_csv('ALL_Entities.csv', index=True)
    driver.quit()
    return df_results

if __name__ == '__main__':
    first_name = "john"  # Replace with the desired first name
    last_name = "doe"    # Replace with the desired last name
    result = nsopw_search(first_name, last_name)
    print(result)


