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


xpath = '//a[@href="javascript:fetchYearData(\'tot20_30\',1)"]'
wait = WebDriverWait(driver, 20)  
element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 
element.click() 
time.sleep(1)

def cathcha_solve_loop():
    for _ in range(15):
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'CaptchaImg/{current_datetime}.png'

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

def extract_text_loop():
    td_elements = driver.find_elements(By.XPATH, "//td[@class='sorting_1']/a")
    for td_element in td_elements:
        text_content = td_element.text
        Cases.append(text_content)
        print("Extracted Text:", text_content)
    
        # Check if the directory exists, if not, create it
        if not os.path.exists('Output'):
            os.makedirs('Output')

        current_date = datetime.now().strftime("%Y-%m-%d") #Assign Current Dates
        csv_file_path = f'Output/{current_date}.csv' #Assign CSV Paths
        if not os.path.isfile(csv_file_path):         # Check if the CSV file existss
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file: # If it doesn't exist, create the file and write header
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['cases'])   # Write header

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file: # Append data to the existing or new CSV file
            csv_writer = csv.writer(csv_file)
            
            for case in Cases:                # Write each row of text_content
                csv_writer.writerow([case])

        print(f"Text content saved to {csv_file_path}")
        # Clear the text_content_list after saving data into CSV
        Cases.clear()

def back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(4)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")
        # Handle the interception issue here if needed

def last_second_back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(3)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_third_back():
    try:
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(2)']")
        back_button.click()
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")

def last_fourth_back():
    try:
        print("Okay")
        back_button = driver.find_element(By.XPATH, "//a[@href='javascript:back(1)']")
        back_button.click()
        print("Clicked")
    except ElementClickInterceptedException as e:
        print(f"Element click intercepted while going back: {e}")
    except TimeoutException as te:
        print(f"TimeoutException while going back: {te}")

Cases = []


def fourth_loop():
    xpath = "(//tbody[@id='est_report_body']/tr/td[4]/a)"
    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    for element in elements:
        time.sleep(0.5)
        element.click()
        time.sleep(1)
        cathcha_solve_loop() 
        extract_text_loop()
        time.sleep(0.5)
        back()
        time.sleep(2)
    last_second_back()


def third_loop():
    xpath = "(//tbody[@id='dist_report_body']/tr/td[4]/a)"
    wait = WebDriverWait(driver, 20)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    for element in elements:
        time.sleep(1)
        element.click()
        time.sleep(0.5)
        fourth_loop()
        time.sleep(0.5)


def second_loop_both_button_clicked_single_row_column():
    xpath = "(//tbody[@id='state_report_body']/tr/td[4]/a)"
    element = driver.find_element(By.XPATH, xpath)
    element.click()



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