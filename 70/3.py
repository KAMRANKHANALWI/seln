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

# instantiate a Service instance with the path
chrome_service = Service(chrome_driver_path)

# start the driver service
chrome_service.start()

# Pass the service object when creating the Chrome WebDriver instance
driver = webdriver.Chrome(service=chrome_service)

# open the website
driver.get(website_url)
driver.maximize_window()
# scroll the page
driver.execute_script("window.scrollBy(0, 500);")

time.sleep(2)

driver.execute_script("window.scrollBy(0, 100);")

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
element.click()
time.sleep(3)


element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
element1.click()
time.sleep(4)


# element2 = driver.find_element(By.XPATH, "//td/a[contains(@href, \"javascript:fetchDistRecords('20 to 30 Years / 1994'\")]")
element2 = driver.find_element(By.LINK_TEXT, "23")
element2.click()
time.sleep(5)

element3 = driver.find_element(By.XPATH, '//*[@id="dist_report_body"]/tr[3]/td[4]/a')
# element3 = driver.find_element(By.LINK_TEXT, "1")
element3.click()
time.sleep(6)


# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(3)    

time.sleep(4)

# Find all table rows using XPath
table_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")

Establishment = []
Civil = []
Criminal = []
Both_Count = []

# Iterate through each table row 
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
df.to_csv('cases_data_3.csv', index=False)
print(df)