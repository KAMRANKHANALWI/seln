import csv
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

element3 = driver.find_element(By.XPATH, '//*[@id="dist_report_body"]/tr[4]/td[4]/a')
# element3 = driver.find_element(By.LINK_TEXT, "1C")
element3.click()
time.sleep(2)


# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")

time.sleep(40)


# //div[@id="part1"]/div[1]/span[2]/text() 
CaseType = []
# //div[@id="part1"]/div[1]/span[3]/text() 
FilingNumber = []
# //div[@id="part1"]/div[1]/span[3]/span[2]/text() 
FilingDate = []
# //div[@id="part1"]/div[1]/span[4]/label 
RegistrationNumber = []
# //div[@id="part1"]/div[1]/span[4]/span[2]/label[2] 
RegistrationDate = []
# //div[@id="part1"]/div/b/span/text() 
CNR_Number = []

# XPath = //span/label/strong[2]
FirstHearingDate = []
NextHearingDate = []
StageOfCase = []
CourtNumberAndJudge = []

# XPath = //span[@class="Petitioner_Advocate_table"]
PetitionerAndAdvocate = []

# XPath = //span[@class="Respondent_Advocate_table"]
RespondentAndAdvocate = []

print('entering loop')

# Wait for the presence of the iframe with a timeout of 10 seconds
wait = WebDriverWait(driver, 10)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))

# Switch to the iframe
driver.switch_to.frame(iframe)

# # Now you can find the element within the iframe
# # Case Details
# case_details_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style=" height:80px; width:700px; "]')))
# # Once the element is located, you can proceed with extracting its text
# case_details_text = case_details_div.text
# print(case_details_text)

# # Case Status
# case_status_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style="width:700px;margin-top:0px;background-color:#FBF6D9;font-size:1em ;font-weight:200;color:red;text-align:center;"]')))
# # Once the element is located, you can proceed with extracting its text
# case_status_text = case_status_div.text
# print(case_status_text)

# # Petitioner
# petitioner_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style="width:700px;margin-top:10px;"]/span[1]')))
# # Once the element is located, you can proceed with extracting its text
# petitioner_text = petitioner_div.text
# print(petitioner_text)

# # Respondent
# respondent_div = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style="width:700px;margin-top:10px;"]/span[2]')))
# # Once the element is located, you can proceed with extracting its text
# respondent_text = respondent_div.text
# print(respondent_text)

try:
    case_type_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[2]')))
    case_type = case_type_element.text.split(":")[-1].strip()
    print(case_type)
    filing_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]')))
    filing_number = filing_number_element.text.split(":")[-1].strip()
    print(filing_number)
    filing_date_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]/span[2]')))
    filing_date = filing_date_element.text.split(":")[-1].strip()
    print(filing_date)
    registration_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/label')))
    registration_number = registration_number_element.text.split(":")[-1].strip()
    print(registration_number)
    registration_date_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/span[2]/label[2]')))
    registration_date = registration_date_element.text.split(":")[-1].strip()
    print(registration_date)
    cnr_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/b/span')))
    cnr_number = cnr_number_element.text.split(":")[-1].strip()
    print(cnr_number)

    # Write the values to a CSV file
    with open('case_details_old.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Case Type', 'Filing Number', 'Filing Date', 'Registration Number', 'Registration Date', 'CNR Number'])
        writer.writerow([case_type, filing_number, filing_date, registration_number, registration_date, cnr_number])

except TimeoutException:
    print("Timeout occurred while waiting for the elements to load.")

# After you finish working with elements inside the iframe, you should switch back to the default content
driver.switch_to.default_content()

driver.quit()
chrome_service.stop()

# # save to csv
# df = pd.DataFrame({'Establishment' : Establishment, 'Civil' : Civil, 'Criminal' : Criminal, 'Both_Count' : Both_Count})
# df.to_csv('cases_data_7.csv', index=False)
# print(df)