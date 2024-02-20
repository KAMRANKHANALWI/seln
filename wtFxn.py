import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoSuchElementException

from datetime import datetime
import pandas as pd
import os
import re
from io import BytesIO
from PIL import Image
import pytesseract

# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Fxn to capture and process captcha
def process_captcha():
    try:
        # Wait until the image element is located
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='captcha_image1']"))
        )

        # Capture the image element
        location = image_element.location
        size = image_element.size

        # Capture screenshot
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot))

        # Calculate cropping coordinates
        left = location['x'] + 250
        top = location['y'] + 400
        right = left + size['width'] + 150
        bottom = top + size['height'] + 100

        # Crop image
        cropped_image = image.crop((left, top, right, bottom))

        # Save cropped image
        current_datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'CaptchaImg/{current_datetime}.png'
        cropped_image.save(img_download_path)

        # Perform OCR on cropped image and remove unwanted characters
        text = pytesseract.image_to_string(cropped_image)
        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove unwanted characters

        # Fill captcha input with extracted text
        captcha_input = driver.find_element(By.ID, "captcha1")
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred while processing captcha: {e}")

# Main script
try:
    url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'

    # Open the website
    driver.get(url)
    driver.maximize_window()

    # Scroll the page
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

    # Choose 600 cases 
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")))
    element.click()
    time.sleep(2)

    # Scroll the page
    driver.execute_script("window.scrollBy(0, 500);")

    # Create an empty list to store DataFrames for each iteration
    dfs = []

    # Iterate through each table row 
    for row in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="example_year"]/tbody/tr'))):
        print(row.text)
        row.find_element(By.XPATH, './td[4]/a').click()
        time.sleep(2)

        # Scroll the page
        driver.execute_script("window.scrollBy(0, 500);")

        # Iterate through each table row 
        for row in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//table[@id="example_state"]/tbody/tr'))):
            print(row.text)
            row.find_element(By.XPATH, './td[4]/a').click()
            time.sleep(1)

            # Scroll the page
            driver.execute_script("window.scrollBy(0, 500);")

            # Iterate through each table row 
            for row in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody[@id="dist_report_body"]/tr'))):
                print(row.text)

                row.find_element(By.XPATH, './td[4]/a').click()
                time.sleep(1)

                # Scroll the page
                driver.execute_script("window.scrollBy(0, 500);")

                # Iterate through each table row 
                for row in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='est_report_body']/tr"))):
                    row.find_element(By.XPATH, './td[4]/a').click()

                    # Check if the directory exists, if not, create it
                    if not os.path.exists('CaptchaImg'):
                        os.makedirs('CaptchaImg')

                    # Call the function
                    process_captcha()

                    Cases = []
                    
                    # Extract Data : Case Table
                    for row in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='cases_report_body']/tr"))):
                        cases = row.find_element(By.XPATH, './td[1]').text
                        Cases.append(cases)
                        print(cases)
                        
                    # Go back 4 levels : cases table 
                    driver.execute_script("window.history.go(-1);")

                # Go back 3 levels : court level
                driver.execute_script("window.history.go(-1);")

            # Go back 2 levels : district level
            driver.execute_script("window.history.go(-1);")

        # Go back 1 level : state level
        driver.execute_script("window.history.go(-1);")

finally:
    # Quit the WebDriver session
    driver.quit()

    # Concatenate all DataFrames in dfs list
    final_df = pd.concat(dfs, ignore_index=True)

    # Save to CSV
    final_df.to_csv('cases.csv', index=False)
    print("done csv")
    print(final_df)
