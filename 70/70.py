from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time


website_url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
chrome_driver_path = '/Users/kamrankhanalwi/Desktop/seln/chromedriver/chromedriver'

chrome_service = Service(chrome_driver_path)
chrome_service.start()
driver = webdriver.Chrome(service=chrome_service)

driver.get(website_url)
driver.maximize_window()
driver.execute_script("window.scrollBy(0, 500);")

time.sleep(2)

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600 cases 
element.click()
time.sleep(2)

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)  

element1 = driver.find_element(By.XPATH, '//*[@id="state_report_body"]/tr[10]/td[4]/a')
# 145
element1.click()
time.sleep(2)

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element2 = driver.find_element(By.LINK_TEXT, "146")
element2.click()
time.sleep(2)

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)  

element3 = driver.find_element(By.XPATH, '//*[@id="dist_report_body"]/tr[10]/td[4]/a')
# element3 = driver.find_element(By.LINK_TEXT, "12B")
element3.click()
time.sleep(2)

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)    

table_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")

Establishment = []
Civil = []
Criminal = []
Both_Count = []

for row in table_rows:
    # print(row.text)
    Establishment.append(row.find_element(By.XPATH, './td[1]').text)
    # home_team.append(row.find_element(By.XPATH, './td[2]').text)
    civ = row.find_element(By.XPATH, './td[2]').text
    Civil.append(civ)
    print(civ)
    Criminal.append(row.find_element(By.XPATH, './td[3]').text)
    Both_Count.append(row.find_element(By.XPATH, './td[4]').text)


driver.quit()
chrome_service.stop()

# save to csv
df = pd.DataFrame({'Establishment' : Establishment, 'Civil' : Civil, 'Criminal' : Criminal, 'Both_Count' : Both_Count})
df.to_csv('cases_data_70.csv', index=False)
print(df)