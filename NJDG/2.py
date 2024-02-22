import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from datetime import datetime
import csv
import os
from io import BytesIO
from PIL import Image
import pytesseract

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def format_date_string(date_string):
    # Split the date string into day, month, and year
    day, month, year = date_string.split()

    # Remove the suffix (e.g., 'th', 'st', 'nd', 'rd') from the day
    day = day[:-2] if day[-2:] in ['th', 'st', 'nd', 'rd'] else day

    # Convert month name to its respective integer value
    month = datetime.strptime(month, '%B').month

    # Format the date string as DD-MM-YYYY
    formatted_date = "{:02d}-{:02d}-{}".format(int(day), month, year)

    return formatted_date  

def scrape_case_details(driver):
    try:
        wait = WebDriverWait(driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))
        driver.switch_to.frame(iframe)

        # Extracting case details
        courtName_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[@class="h1class"]/span')))
        courtName = courtName_element.text
        print(courtName)
        case_type_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[2]')))
        case_type = case_type_element.text.split(":")[-1].strip()
        print(case_type)
        filing_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]')))
        filing_number = filing_number_element.text.split(":")[-1].strip()
        print(filing_number)
        filing_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]/span[2]')))
        filing_date = filing_date_element.text.split(":")[-1].strip()
        print(filing_date)
        registration_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/label')))
        registration_number = registration_number_element.text.split(":")[-1].strip()
        print(registration_number)
        registration_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/span[2]/label[2]')))
        registration_date = registration_date_element.text.split(":")[-1].strip()
        print(registration_date)
        cnr_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/b/span')))
        cnr_number = cnr_number_element.text.split(":")[-1].strip()
        print(cnr_number)

        firstDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[1]/label/strong[2]')))
        firstDate = ":".join(firstDate_element.text.strip().split(":")[1:]).strip()
        firstDate = format_date_string(firstDate)
        print(firstDate)
        nextDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[2]/label/strong[2]')))
        nextDate = ":".join(nextDate_element.text.strip().split(":")[1:]).strip()
        nextDate = format_date_string(nextDate)
        print(nextDate)
        stage_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[3]/label/strong[2]')))
        stage = stage_element.text.split(":")[-1].strip()
        print(stage)
        judge_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[4]/label/strong[2]')))
        judge = judge_element.text.split(":")[-1].strip()
        print(judge)

        # petitioner and advocate
        span_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="Petitioner_Advocate_table"]')))
        span_content = span_element.text
        lines_p = span_content.split('\n\n')
        # Initialize variables outside the if statement
        pet_advocate = ""
        petitioner = lines_p[0].strip()  
        if len(lines_p) > 1:
            pet_advocate = "- ".join(lines_p[1].split("- ")[1:]).strip()


        # Respondent and Advocate
        respondent_element = driver.find_element(By.XPATH, '//span[@class="Respondent_Advocate_table"]')
        respondent_content = respondent_element.text
        lines_r = respondent_content.split('\n\n')
        print(lines_r)
        # Initialize variables outside the if statement
        res_advocate = ""

        # Extract petitioner and advocate information
        respondent = lines_r[0].strip()  
        if len(lines_r) > 1:
            res_advocate = "- ".join(lines_r[1].split("- ")[1:]).strip()
        
        print("Respondent:", respondent)
        print("Advocate:", res_advocate)
        
        # Save data to CSV file
        if not os.path.exists('CASES_DATA'):
            os.makedirs('CASES_DATA')
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_file_path = f'CASES_DATA/{current_date}.csv'

        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Court Name', 'Case Type', 'Filing Number', 'Filing Date', 'Registration Number', 'Registration Date', 'CNR Number', 'First Hearing Date', 'Next Hearing Date', 'Stage of Case', 'Court Number and Judge', 'Petitioner', 'P Advocate', 'Respondent', 'R Advocate'])

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([courtName, case_type, filing_number, filing_date, registration_number, registration_date, cnr_number, firstDate, nextDate, stage, judge, petitioner, pet_advocate, respondent, res_advocate])

        print(f"Case details saved to {csv_file_path}")

    except TimeoutException:
        print("Timeout occurred while waiting for the elements to load.")

    finally:
        driver.switch_to.default_content()


url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
driver.get(url)
driver.maximize_window() 
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)


element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600 cases 
element.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)  

element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
element1.click()
time.sleep(1)
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(1)

element2 = driver.find_element(By.LINK_TEXT, "23")
element2.click()
time.sleep(1)

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(1)  

element3 = driver.find_element(By.LINK_TEXT, "19")
element3.click()
time.sleep(2)


# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")

time.sleep(50)

print('IN IFRAME')

scrape_case_details(driver)

driver.quit()


