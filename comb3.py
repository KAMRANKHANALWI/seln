import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException, NoSuchElementException, ElementNotInteractableException

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
# def process_captcha():
#     try:
#         for _ in range(10):  # Try processing captcha multiple times
#             # Wait until the image element is located
#             image_element = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//img[@id='captcha_image1']"))
#             )

#             # Capture the image element
#             location = image_element.location
#             size = image_element.size

#             # Capture screenshot
#             screenshot = driver.get_screenshot_as_png()
#             image = Image.open(BytesIO(screenshot))

#             # Calculate cropping coordinates
#             left = location['x'] + 250
#             top = location['y'] + 400
#             right = left + size['width'] + 150
#             bottom = top + size['height'] + 100

#             # Crop image
#             cropped_image = image.crop((left, top, right, bottom))

#             # Save cropped image
#             current_datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
#             img_download_path = f'CaptchaImg/{current_datetime}.png'
#             cropped_image.save(img_download_path)

#             # Perform OCR on cropped image and remove unwanted characters
#             text = pytesseract.image_to_string(cropped_image)
#             cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove unwanted characters

#             # Fill captcha input with extracted text
#             captcha_input = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.ID, "captcha1"))
#             )
#             captcha_input.clear()
#             captcha_input.send_keys(cleaned_text)

#             # submit button
#             submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')))
#             submit_button.click()
#             time.sleep(5)
#             print("Captcha processing completed.")

#             # Check if the table appears after successful submission
#             if driver.find_elements(By.XPATH, '//table[@id="example_cases"]'):
#                 print("Submission successful. Stopping captcha processing loop.")
#                 return True  # Submission successful, exit the function
            

#             # Check for alert
#             popup_timeout = 10
#             try:
#                 popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
#                 popup.accept()
#                 time.sleep(3)
#                 print("Alert accepted.")
#             except:
#                 print("No alert found within the specified timeout or alert already dismissed.")

#         # If the loop completes without successful submission
#         print("Captcha processing loop completed without successful submission.")
#         return False

#     except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
#         print(f"An error occurred while processing captcha: {e}")
#         return False
#     except UnexpectedAlertPresentException as alert_ex:
#         print("Alert Present:", alert_ex)
#         # Handle the alert by accepting it
#         driver.switch_to.alert.accept()
#         return False

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

# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

# Fxn to iterate through each level's table 
    
# Define the array of XPaths
xpath_list = [
    '//table[@id="example_year"]/tbody',
    '//table[@id="example_state"]/tbody',
    '//tbody[@id="dist_report_body"]',
    "//tbody[@id='est_report_body']",
    '//tbody[@id="cases_report_body"]'
]
# print(len(xpath_list))
# # Recursive function to iterate through tables
# def iterate_through_tables(xpath_list, current_level=0):
#     if current_level >= len(xpath_list):
#         return

#     # Retrieve XPath for the current level
#     xpath = xpath_list[current_level]

#     # Wait until the table element is located
#     table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
#     table_rows = table.find_elements(By.TAG_NAME, "tr")
    
#     # Iterate through each table row 
#     for row in table_rows:
#         print(row.text)
#         # Click on a specific element within the row
#         link_element_xpath = './/td[4]/a'  # Adjusted XPath
#         WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, link_element_xpath))).click()
#         print(f'clicked {xpath}')
#         time.sleep(2)  # Adjust sleep time as needed

#         # Scroll the page
#         scroll_down_500()

#         # Recursive call for the next level table
#         iterate_through_tables(xpath_list, current_level + 1)

#     # After processing the lower level, go back to the current level
#     # go_back(current_level)
#     driver.execute_script("window.history.go(-1);")

Cases = []

# Recursive function to iterate through tables
def iterate_through_tables(xpath_list, current_level=0):
    if current_level >= len(xpath_list):
        return

    # Retrieve XPath for the current level
    xpath = xpath_list[current_level]

    # Wait until the table element is located
    table = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    table_rows = table.find_elements(By.TAG_NAME, "tr")
    
    # Iterate through each table row 
    for row in table_rows:
        print(row.text)
        # Click on a specific element within the row
        link_element_xpath = './/td[4]/a'  # Adjusted XPath
        WebDriverWait(row, 10).until(EC.element_to_be_clickable((By.XPATH, link_element_xpath))).click()
        print(f'clicked {xpath}')
        time.sleep(2)  # Adjust sleep time as needed

        # Scroll the page
        scroll_down_500()

        # Process captcha at the last level
        if current_level == len(xpath_list) - 2:
            # process_captcha()
            # time.sleep(2)  # Adjust sleep time as needed

            # Process captcha multiple times
            for _ in range(10):
                try:
                    process_captcha()

                    # submit button
                    submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')))
                    submit_button.click()
                    time.sleep(5)
                    print("Captcha processing completed.")
                    
                    # Check for alert
                    popup_timeout = 10
                    try:
                        popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
                        popup.accept()
                        time.sleep(3)
                        print("Alert accepted.")
                    except:
                        print("No alert found within the specified timeout or alert already dismissed.")

                except UnexpectedAlertPresentException as alert_ex:
                    print("Alert Present:", alert_ex)
                    # Handle the alert by accepting it
                    driver.switch_to.alert.accept()


        # Extract text if needed
        if current_level < len(xpath_list) - 1:
            # Add extraction logic here
            # pass
            Cases = []
                    
            # Extract Data : Case Table
            cases = iterate_through_tables(xpath_list, 4)
            for case in cases:
                Cases.append(case.text)

        # Recursive call for the next level table
        iterate_through_tables(xpath_list, current_level + 1)

    # After processing the lower level, go back to the current level
    driver.execute_script("window.history.go(-1);")


# # Starting point of the recursive loop
# iterate_through_tables(xpath_list, 0)

# # Go back 4 levels : cases table 
#                     driver.execute_script("window.history.go(-1);")

#                 # Go back 3 levels : court level
#                 driver.execute_script("window.history.go(-1);")

#             # Go back 2 levels : district level
#             driver.execute_script("window.history.go(-1);")

#         # Go back 1 level : state level
#         driver.execute_script("window.history.go(-1);")


# Fxn to go back
def go_back(level):
    try:
        xpath = f'//a[@href="javascript:back({level})"]'
        back_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        back_button.click()
        scroll_down_500()
        time.sleep(1)
    except Exception as e:
        print(f"An error occurred while going back: {e}")


current_datetime = datetime.now()  # Get the current date and time

url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'


# Main script

try:
    # open the website
    driver.get(url)
    driver.maximize_window()
    # scroll the page
    scroll_down_500()
    # Choose 600 cases 
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")))
    element.click()
    time.sleep(2)
    # scroll the page
    scroll_down_500() 
    iterate_through_tables(xpath_list, 0)
        
finally:
    # Quit the WebDriver session
    driver.quit()

    # Concatenate all DataFrames in dfs list
    final_df = pd.concat(dfs, ignore_index=True)

    # Save to CSV
    final_df.to_csv('cases.csv', index=False)
    print("done csv")
    print(final_df)