import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import os
import re
from io import BytesIO
from PIL import Image
import pytesseract

# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'https://njdg.ecourts.gov.in/hcnjdg_public/civil/o_civil_case_history.php?es_flag=Y&state_code=13&dist_code=1&court_code=1&case_number=212400007782023&type=both&objection1=totalpending_cases&matchtotal=13145&jocode=XX0001&court_no=5128&cino=UPHC010057921994&disposed_case=N'


# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)


# Main script
driver.get(url)
driver.maximize_window()
# Scroll the page
scroll_down_500()
time.sleep(15)

# //div[@id="part1"]/form/div[1]

time.sleep(5)

# Find all table rows using XPath
# table_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")

# //*[@id="part1"]/form/div[1]/span[2]/text() 
CaseType = []
# //*[@id="part1"]/form/div[1]/span[3] 
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

try:
# Find the case details
    case_type_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/span[2]')))
    case_type = case_type_element.text.split(":")[-1].strip()
    print(case_type)
    filing_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/span[3]')))
    filing_number = filing_number_element.text.split(":")[-1].strip()
    print(filing_number)
    filing_date_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/span[3]/span[2]')))
    filing_date = filing_date_element.text.split(":")[-1].strip()
    print(filing_date)
    registration_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/span[4]/label')))
    registration_number = registration_number_element.text.split(":")[-1].strip()
    print(registration_number)
    registration_date_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/span[4]/span[2]/label[2]')))
    registration_date = registration_date_element.text.split(":")[-1].strip()
    print(registration_date)
    cnr_number_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/form/div[1]/b/span')))
    cnr_number = cnr_number_element.text.split(":")[-1].strip()
    print(cnr_number)

    # Write the values to a CSV file
    with open('case_details.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Case Type', 'Filing Number', 'Filing Date', 'Registration Number', 'Registration Date', 'CNR Number'])
        writer.writerow([case_type, filing_number, filing_date, registration_number, registration_date, cnr_number])

except TimeoutException:
    print("Timeout occurred while waiting for the elements to load.")

driver.quit()