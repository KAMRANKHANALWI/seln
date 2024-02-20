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

# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

# Fxn to go back
def go_back(level):
    xpath = f'//a[@href="javascript:back({level})"]'
    back_button = driver.find_element(By.XPATH, xpath)
    back_button.click()
    scroll_down_500()
    time.sleep(1)

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
    # element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
    element.click()
    time.sleep(2)

    # scroll the page
    scroll_down_500() 

    # Create an empty list to store DataFrames for each iteration
    dfs = []

    # table1_rows = driver.find_elements(By.XPATH, '//table[@id="example_year"]/tbody/tr')
    table1_rows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="example_year"]/tbody/tr')))
    # Iterate through each table row 
    for row in table1_rows:
        print(row.text)
        row.find_element(By.XPATH, './td[4]/a').click()
        # 23
        print('clicked table 1')
        time.sleep(2)

        # scroll the page
        scroll_down_500()

        # State Level 
        # table2_rows = driver.find_elements(By.XPATH, '//table[@id="example_state"]/tbody/tr')
        table2_rows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="example_state"]/tbody/tr')))
        # Iterate through each table row 
        for row in table2_rows:
            print(row.text)
            row.find_element(By.XPATH, './td[4]/a').click()
            # 23
            print('clicked table 2')
            time.sleep(1)

            # scroll the page
            scroll_down_500()

            # District Level 
            # table3_rows = driver.find_elements(By.XPATH, '//tbody[@id="dist_report_body"]/tr')
            table3_rows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//tbody[@id="dist_report_body"]/tr')))

            # Iterate through each table row 
            for row in table3_rows:
                print(row.text)

                row.find_element(By.XPATH, './td[4]/a').click()
                # 19
                print('clicked table 3')
                time.sleep(1)

                # scroll the page
                scroll_down_500()   

                # Court Level
                # table4_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")
                table4_rows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='est_report_body']/tr")))

                # Create an empty list to store Cases for each iteration
                Cases = []

                # court table iteration
                # Iterate through each table row 
                for row in table4_rows:
                    # print(row.text)
                    # opens cases table by clicking
                    row.find_element(By.XPATH, './td[4]/a').click() # 1
                    print('clicked table 4')

                    # Check if the directory exists, if not, create it
                    if not os.path.exists('CaptchaImg'):
                        os.makedirs('CaptchaImg')

                    # # Process captcha multiple times
                    # for _ in range(15):
                    #     try:
                    #         process_captcha()

                    #         # submit button
                    #         submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')))
                    #         time.sleep(2)
                    #         submit_button.click()
                    #         time.sleep(5)
                    #         print("Captcha processing completed.")
                            
                    #         # Check for alert
                    #         popup_timeout = 10
                    #         try:
                    #             popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
                    #             popup.accept()
                    #             time.sleep(3)
                    #             print("Alert accepted.")
                    #         except:
                    #             print("No alert found within the specified timeout or alert already dismissed.")

                    #     except UnexpectedAlertPresentException as alert_ex:
                    #         print("Alert Present:", alert_ex)
                    #         # Handle the alert by accepting it
                    #         driver.switch_to.alert.accept()
                        
                    # Process captcha multiple times
                    success = False
                    for _ in range(10):
                        try:
                            process_captcha()

                            # submit button
                            submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')))
                            submit_button.click()
                            time.sleep(5)
                            print("Captcha processing completed.")
                            
                            # Check if the table appears after successful submission
                            if driver.find_elements(By.XPATH, '//table[@id="example_cases"]'):
                                print("Submission successful. Stopping captcha processing loop.")
                                success = True  # Submission successful, exit the loop
                                break

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

                    if not success:
                        print("Submission unsuccessful after 10 attempts.")


                    Cases = []
                    
                    # Extract Data : Case Table
                    # cases_rows = driver.find_elements(By.XPATH, "//tbody[@id='cases_report_body']/tr")
                    cases_rows = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='cases_report_body']/tr")))
                    # Iterate through each case table row
                    for row in cases_rows:
                        print(row.text)
                        cases = row.find_element(By.XPATH, './td[1]').text
                        Cases.append(cases)
                        print(cases)
                        # Cases.append(row.find_element(By.XPATH, './td[1]').text)
                        
                    go_back(4)  # Goes back 4 levels : cases table 

                # Create DataFrame for each iteration and append to dfs list
                df = pd.DataFrame({'Cases': Cases})
                dfs.append(df)
                
                go_back(3) # Goes back 3 levels : court level

            go_back(2)  # Goes back 2 levels : district level

        go_back(1)  # Goes back 1 level : state level
        
finally:
    # Quit the WebDriver session
    driver.quit()

    # Concatenate all DataFrames in dfs list
    final_df = pd.concat(dfs, ignore_index=True)

    # Save to CSV
    final_df.to_csv('cases.csv', index=False)
    print("done csv")
    print(final_df)