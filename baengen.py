from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import csv
from datetime import datetime
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

from datetime import datetime

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

def format_date(date_string):
    # Split the date string into day, month, and year
    day, month, year = date_string.split()

    # Remove the suffix (e.g., 'th', 'st', 'nd', 'rd') from the day
    day = day[:-2] if day[-2:] in ['th', 'st', 'nd', 'rd'] else day

    # Convert month name to its respective integer value
    month = datetime.strptime(month, '%B').month

    # Convert day, month, and year to integers
    day = int(day)
    month = int(month)
    year = int(year)

    # Format the day and month with leading zeros if necessary
    formatted_day = "{:02d}".format(day)
    formatted_month = "{:02d}".format(month)

    return formatted_day, formatted_month, year

def parse_date_string(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, '%d-%m-%Y')

    # Extract day, month, and year from the datetime object
    day = date_object.day
    month = date_object.month
    year = date_object.year

    # Format the day and month with leading zeros if necessary
    formatted_day = "{:02d}".format(day)
    formatted_month = "{:02d}".format(month)

    return formatted_day, formatted_month, year

print('entering loop')

# Wait for the presence of the iframe with a timeout of 10 seconds
wait = WebDriverWait(driver, 10)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))

# Switch to the iframe
driver.switch_to.frame(iframe)

try:
    wait = WebDriverWait(driver, 10)
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
    file_day, file_month, file_year = parse_date_string(filing_date)
    print(filing_date)
    print(file_day)
    print(file_month)
    print(file_year)
    registration_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/label')))
    registration_number = registration_number_element.text.split(":")[-1].strip()
    print(registration_number)
    registration_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/span[2]/label[2]')))
    registration_date = registration_date_element.text.split(":")[-1].strip()
    reg_day, reg_month, reg_year = parse_date_string(registration_date)
    print(registration_date)
    print(reg_day)
    print(reg_month)
    print(reg_year)
    cnr_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/b/span')))
    cnr_number = cnr_number_element.text.split(":")[-1].strip()
    print(cnr_number)

    firstDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[1]/label/strong[2]')))
    firstDateSrt = ":".join(firstDate_element.text.strip().split(":")[1:]).strip()
    firstDate = format_date_string(firstDateSrt)
    f_day, f_month, f_year = format_date(firstDateSrt)
    print(firstDate)
    print(f_day)
    print(f_month)
    print(f_year)
    nextDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[2]/label/strong[2]')))
    nextDateStr = ":".join(nextDate_element.text.strip().split(":")[1:]).strip()
    nextDate = format_date_string(nextDateStr)
    n_day, n_month, n_year = format_date(nextDateStr)
    print(nextDate)
    print(n_day)
    print(n_month)
    print(n_year)
    stage_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[3]/label/strong[2]')))
    stage = stage_element.text.split(":")[-1].strip()
    print(stage)
    judge_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[4]/label/strong[2]')))
    judge = judge_element.text.split(":")[-1].strip()
    print(judge)

    # Petitioner and Advocate
    span_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="Petitioner_Advocate_table"]')))
    span_content = span_element.text
    lines_p = span_content.split('\n\n')
    print(lines_p)
    print("P Lines: ", len(lines_p))
    # Initialize variables outside the if statement
    pet_advocate = ""
    # Extract petitioner and advocate information
    petitioner = lines_p[0].strip()  
    if len(lines_p) > 1:
        pet_advocate = "- ".join(lines_p[1].split("- ")[1:]).strip()
    print("Petitioner:", petitioner)
    print("Advocate:", pet_advocate)

    # Respondent and Advocate
    respondent_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="Respondent_Advocate_table"]')))
    respondent_content = respondent_element.text
    lines_r = respondent_content.split('\n\n')
    print(lines_r)
    print("R Lines: " ,len(lines_r))
    # Initialize variables outside the if statement
    res_advocate = ""
    # Extract respondent and advocate information
    respondent = lines_r[0].strip()  
    if len(lines_r) > 1:
        res_advocate = "- ".join(lines_r[1].split("- ")[1:]).strip()
    
    print("Respondent:", respondent)
    print("Advocate:", res_advocate)

    # CSV file Save in Date & Time Format 
    # Check if the directory exists, if not, create it
    if not os.path.exists('CSV_DATA'):
        os.makedirs('CSV_DATA')
    
    # Assign Current Date
    current_date = datetime.now().strftime("%Y-%m-%d")
    csv_file_path = f'CSV_DATA/{current_date}.csv'

    # Check if the CSV file exists
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Court Name' ,'Case Type', 'Filing Number', 'Filing Date', 'Day', 'Month', 'Year', 'Registration Number', 'Registration Date', 'Day', 'Month', 'Year', 'CNR Number', 'First Hearing Date', 'Day', 'Month', 'Year', 'Next Hearing Date', 'Day', 'Month', 'Year', 'Stage of Case', 'Court Number and Judge', 'Petitioner ', 'P Advocate', 'Respondent', 'R Advocate'])

    # Append data to the CSV file
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([courtName ,case_type, filing_number, filing_date, file_day, file_month, file_year, registration_number, registration_date, reg_day, reg_month, reg_year, cnr_number, firstDate, f_day, f_month, f_year , nextDate, n_day, n_month, n_year ,stage, judge, petitioner, pet_advocate, respondent, res_advocate])

    print(f"Case details saved to {csv_file_path}")

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