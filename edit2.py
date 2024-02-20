import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600 cases
element.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element1 = driver.find_element(By.XPATH, '//*[@id="state_report_body"]/tr[2]/td[4]/a')
# 17
element1.click()
time.sleep(2)

# scroll the page
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element2 = driver.find_element(By.LINK_TEXT, "17")
element2.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element3 = driver.find_element(By.XPATH, '//*[@id="dist_report_body"]/tr[1]/td[4]/a')
element3.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

# Find all table rows using XPath
table_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")

# Create an empty list to store DataFrames for each iteration
dfs = []

# Iterate through each table row
for row in table_rows:
    row.find_element(By.XPATH, './td[4]/a').click()
    print('clicked')
    time.sleep(15)

    submit_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')
    time.sleep(2)
    submit_button.click()
    time.sleep(5)

    cases_rows = driver.find_elements(By.XPATH, "//tbody[@id='cases_report_body']/tr")

    Cases = []

    # Iterate through each case table row
    for row in cases_rows:
        cases = row.find_element(By.XPATH, './td[1]').text
        Cases.append(cases)

    back_4 = driver.find_element(By.XPATH, '//a[@href="javascript:back(4)"]')
    back_4.click()
    time.sleep(2)

    # Create DataFrame for each iteration and append to dfs list
    df = pd.DataFrame({'Cases': Cases})
    dfs.append(df)

driver.quit()
chrome_service.stop()

# Concatenate all DataFrames in dfs list
final_df = pd.concat(dfs, ignore_index=True)

# Save to CSV
final_df.to_csv('cases.csv', index=False)
print("done csv")
print(final_df)
