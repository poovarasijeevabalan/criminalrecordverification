from selenium import webdriver
from selenium.webdriver.common.by import By

def DOB_Extraction(url, state_code):

  try:
    driver = webdriver.Chrome()  
    driver.get(url)
    

    if state_code == 'CA':
      dob_element = driver.find_element(By.XPATH, "//td[@id='PDOB']")
      dob_match = dob_element.text

    elif state_code == 'TX':
      dob_element = driver.find_element(By.XPATH, "//h2[text()= 'Birth Date(s)']//following::ul")
      dob_match = dob_element.text

    elif state_code == 'PA':
      try:
        Accept_element = driver.find_element(By.XPATH, "//h2[text()= 'Birth Date(s)']//following::ul")
        Accept_element.click()
      except:
        print("disclaimer page not found")
      dob_element = driver.find_element(By.XPATH, "//div[@class='row offenderDataRow']/div[@class='col-sm-7ths']/dl[dt[contains(text(), 'Birth Year')]]/dd")
      dob_match = dob_element.text

    

    if dob_match:
      return dob_match
    else:
      return "NA"
  except:
     return 'Error'


if __name__ == "__main__":
  url = "https://meganslaw.ca.gov/OffenderDisplay.aspx?searchby=offender&ID=18605142J7721&NSOPRFlag=True"
  DOB_Extraction(url)


   