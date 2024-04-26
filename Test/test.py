from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = "https://www.zaubacorp.com/company/TANAGER/F04044"

driver.get(url)

enter_company = driver.find_element(By.XPATH, "//input[@placeholder='Enter company name or cin']")
enter_company.send_keys("Tata")

time.sleep(5)

driver.quit()