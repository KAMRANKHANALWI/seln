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

url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
driver.get(url)
driver.maximize_window() 
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)

''' STEP 1 == Clicking on 20-30 year Total link'''
xpath = '//a[@href="javascript:fetchYearData(\'tot20_30\',1)"]'
wait = WebDriverWait(driver, 20)  
element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 
element.click() 
time.sleep(1)

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

'''STEP 9 == Filling Captcha Image - 2 '''
def cathcha2_solve_loop():
    for _ in range(15):
        # Check if the directory exists, if not, create it
        if not os.path.exists('Captcha2Img'):
            os.makedirs('Captcha2Img')

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'Captcha2Img/{current_datetime}.png'

        image_element = driver.find_element(By.XPATH, "//img[@id='captcha_image']")
        location = image_element.location
        size = image_element.size
        screenshot = driver.get_screenshot_as_png() # Capture the screenshot of the entire browser window
        image = Image.open(BytesIO(screenshot)) # Use Pillow to open the screenshot and crop the desired area
        # Calculate cropping coordinates
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        # left = location['x'] + 250  
        # top = location['y'] + 400
        # right = left + size['width'] + 150
        # bottom = top + size['height'] + 100

        cropped_image = image.crop((left, top, right, bottom)) 
        cropped_image.save(img_download_path) 
        time.sleep(2)

        '''STEP 10 == Solving the Captcha img for solving'''
        if img_download_path is not None:
            image_path = img_download_path
            image = Image.open(image_path)

            # Perform OCR on the image
            text = pytesseract.image_to_string(image) 
            cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove unwanted characters
            cleaned_text = cleaned_text[:5]
            # print("Extracted Text:", cleaned_text)
        else:
            print("Not Able to find")

        '''STEP 11 == After Solving the Captcha Filling the data captcha data into input & Submit'''
        # Fill captcha input with extracted text
        captcha_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "captcha")))
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)
        time.sleep(3)
        # Submit Button 
        xpath = '//input[@type="submit"]'
        wait = WebDriverWait(driver, 20)  
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 
        element.click() 
        time.sleep(5)

        # # Check for alert
        # popup_timeout = 10
        # try:
        #     popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
        #     popup.accept()
        #     time.sleep(3)
        # except:
        #     print("No alert found within the specified timeout.")
        #     break

'''STEP 6 == Filling Captcha Image - 1 '''
def cathcha1_solve_loop():
    for _ in range(15):
        # Check if the directory exists, if not, create it
        if not os.path.exists('Captcha1Img'):
            os.makedirs('Captcha1Img')

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'Captcha1Img/{current_datetime}.png'

        image_element = driver.find_element(By.XPATH, "//img[@id='captcha_image1']")
        location = image_element.location
        size = image_element.size
        screenshot = driver.get_screenshot_as_png() # Capture the screenshot of the entire browser window
        image = Image.open(BytesIO(screenshot)) # Use Pillow to open the screenshot and crop the desired area
        # Calculate cropping coordinates
        # left = location['x']
        # top = location['y']
        # right = left + size['width']
        # bottom = top + size['height']
        left = location['x'] + 250  
        top = location['y'] + 400
        right = left + size['width'] + 150
        bottom = top + size['height'] + 100

        cropped_image = image.crop((left, top, right, bottom)) 
        cropped_image.save(img_download_path) 
        time.sleep(2)

        '''STEP 7 == Solving the Captcha img for solving'''
        if img_download_path is not None:
            image_path = img_download_path
            image = Image.open(image_path)

            # Perform OCR on the image
            text = pytesseract.image_to_string(image) 
            cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove unwanted characters
            cleaned_text = cleaned_text[:5]
            # print("Extracted Text:", cleaned_text)
        else:
            print("Not Able to find")

        '''STEP 8 == After Solving the Captcha Filling the data captcha data into input & Submit'''
        # Fill captcha input with extracted text
        captcha_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "captcha1")))
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)
        time.sleep(3)

        xpath = '//input[@class="btn btn-success col-auto btn-sm"]'
        wait = WebDriverWait(driver, 20)  
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 
        element.click() 
        time.sleep(3)

        # Check for alert
        popup_timeout = 10
        try:
            popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
            popup.accept()
            time.sleep(3)
        except:
            print("No alert found within the specified timeout.")
            break

def extract_text_loop(driver):
    try:
        wait = WebDriverWait(driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))
        driver.switch_to.frame(iframe)

        # Case Details
        case_type_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[2]')))
        case_type = case_type_element.text.split(":")[-1].strip()
        filing_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]')))
        filing_number = filing_number_element.text.split(":")[-1].strip()
        filing_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]/span[2]')))
        filing_date = filing_date_element.text.split(":")[-1].strip()
        registration_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/label')))
        registration_number = registration_number_element.text.split(":")[-1].strip()
        registration_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[4]/span[2]/label[2]')))
        registration_date = registration_date_element.text.split(":")[-1].strip()
        cnr_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/b/span')))
        cnr_number = cnr_number_element.text.split(":")[-1].strip()

        # Case Status 
        firstDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[1]/label/strong[2]')))
        firstDate = ":".join(firstDate_element.text.strip().split(":")[1:]).strip()
        nextDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[2]/label/strong[2]')))
        nextDate = ":".join(nextDate_element.text.strip().split(":")[1:]).strip()
        stage_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[3]/label/strong[2]')))
        stage = stage_element.text.split(":")[-1].strip()
        judge_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[4]/label/strong[2]')))
        judge = judge_element.text.split(":")[-1].strip()

        # Petitioner and Advocate
        span_element = driver.find_element(By.XPATH, '//span[@class="Petitioner_Advocate_table"]')
        span_content = span_element.text
        lines_p = span_content.split('\n\n')
        petitioner = lines_p[0].strip()
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
                csv_writer.writerow(['Case Type', 'Filing Number', 'Filing Date', 'Registration Number', 'Registration Date', 'CNR Number', 'First Hearing Date', 'Next Hearing Date', 'Stage of Case', 'Court Number and Judge', 'Petitioner ', 'P Advocate', 'Respondent', 'R Advocate'])

        # Append data to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([case_type, filing_number, filing_date, registration_number, registration_date, cnr_number, firstDate, nextDate, stage, judge, petitioner, pet_advocate, respondent, res_advocate])

        print(f"Case details saved to {csv_file_path}")

    except TimeoutException:
        print("Timeout occurred while waiting for the elements to load.")

    finally:
        driver.switch_to.default_content()

def back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(6)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_second_back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(4)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_third_back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(3)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_fourth_back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(2)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_fifth_back():
    try:
        print("Okay")
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(1)']")
        back_button.click()
        print("Clicked")
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")
    except TimeoutException as te:
        print(f"TimeoutException while going back: {te}")

# Cases = []

''' STEP X == Clicking on Cases Table link'''
def fifth_loop():
    xpath = "(//tbody[@id='cases_report_body']/tr/td/a)" 
    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    for element in elements:
        time.sleep(0.5)
        element.click()
        time.sleep(1)
        cathcha2_solve_loop() 
        extract_text_loop(driver)
        time.sleep(0.5)
        back()
        time.sleep(2)
    last_second_back()

''' STEP 5 == Clicking on 20-30 year Total link'''
def fourth_loop():
    xpath = "(//tbody[@id='est_report_body']/tr/td[4]/a)"
    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    for element in elements:
        time.sleep(0.5)
        element.click()
        time.sleep(1)
        cathcha1_solve_loop() 
        fifth_loop()
        time.sleep(0.5)
        back()
        time.sleep(2)
    last_third_back()


''' STEP 4 == Clicking on 20-30 year Total link'''
def third_loop():
    xpath = "(//tbody[@id='dist_report_body']/tr/td[4]/a)"
    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    print("Len", len(elements))
    for element in elements:
        time.sleep(1)
        element.click()
        time.sleep(0.5)
        fourth_loop()
        time.sleep(0.5)
        print("Breaking")
    # print("Total Count of Cases: ",len(Cases))


def second_loop_both_button_clicked_single_row_column():
    xpath = "(//tbody[@id='state_report_body']/tr/td[4]/a)"
    element = driver.find_element(By.XPATH, xpath)
    element.click()


''' STEP 2 == Clicking on 20-30 year Total link'''
def first_loop():
    button_xpath = "(//tbody[@id='state_report_body']/tr/td[4]/a)"
    wait = WebDriverWait(driver, 20)
    try:
        # skip = 1
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, button_xpath)))
        print("Countttt ",len(elements))
        for element in elements:
            # if skip<=3:
            #     skip+=1
            #     continue
            element.click()
            time.sleep(3)
            second_loop_both_button_clicked_single_row_column()
            time.sleep(3)
            third_loop()
            time.sleep(3)
            last_third_back()
            time.sleep(3)
            last_fourth_back()
            time.sleep(3)
    except Exception as e:
        print(f"Error clicking the button: {e}")

first_loop()

time.sleep(20)

driver.quit