import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def cathcha_solve_loop():
    for _ in range(15):
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'CaptchaImg/{current_datetime}.png'

        # image_element = driver.find_element(By.XPATH, "//img[@id='captcha_image1']")
        # Wait until the image element is located
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@id='captcha_image1']"))
        )
        location = image_element.location
        size = image_element.size
        screenshot = driver.get_screenshot_as_png() # Capture the screenshot of the entire browser window

        image = Image.open(BytesIO(screenshot)) # Use Pillow to open the screenshot and crop the desired area
        # left = location['x']
        # top = location['y']
        # right = left + size['width']
        # bottom = top + size['height']

        # Calculate cropping coordinates
        left = location['x'] + 250
        top = location['y'] + 400
        right = left + size['width'] + 150
        bottom = top + size['height'] + 100

        cropped_image = image.crop((left, top, right, bottom)) # Crop the image to the specified area
        cropped_image.save(img_download_path) # Save the cropped image to a file
        time.sleep(2)


        '''STEP 7 == Solving the Captcha img for solving'''
        if img_download_path is not None:
            image_path = img_download_path
            image = Image.open(image_path)

            # Perform OCR on the image
            text = pytesseract.image_to_string(image) 
            cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text)  # Remove unwanted characters
            # print("Extracted Text:", cleaned_text) 
            # text = text[:5]
        else:
            print("Not Able to find")

        '''STEP 8 == After Solving the Captcha Filling the data captcha data into input & Submit'''
        # Fill captcha input with extracted text
        captcha_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "captcha1")))
        # captcha_input = driver.find_element("id", "captcha1")
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)
        time.sleep(3)

        xpath = '//input[@class="btn btn-success col-auto btn-sm"]'
        wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) # Wait until the element is present
        element.click() # Click on the element
        time.sleep(3)
        popup_timeout = 10
        try:
            popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
            popup.accept()
            time.sleep(3)
        except:
            print("No alert found within the specified timeout.")
            break

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
        captcha_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "captcha1"))
        )
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)

    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"An error occurred while processing captcha: {e}")

def scrape_case_details(driver):
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
        # respondent = ""
        res_advocate = ""

        # Extract petitioner and advocate information
        respondent = lines_r[0].strip()  
        # res_advocate = "- ".join(lines_r[1].split("- ")[1:]).strip()
        # print("Respondent:", respondent)
        # print("Advocate:", res_advocate)
        # Check if lines_r has more than one element
        if len(lines_r) > 1:
            res_advocate = "- ".join(lines_r[1].split("- ")[1:]).strip()
        
        print("Respondent:", respondent)
        print("Advocate:", res_advocate)


        # Write the values to a CSV file
        with open('case_info.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Case Type', 'Filing Number', 'Filing Date', 'Registration Number', 'Registration Date', 'CNR Number', 'First Hearing Date', 'Next Hearing Date', 'Stage of Case', 'Court Number and Judge', 'Petitioner ', 'P Advocate', 'Respondent', 'R Advocate'])
            writer.writerow([case_type, filing_number, filing_date, registration_number, registration_date, cnr_number, firstDate, nextDate, stage, judge, petitioner, pet_advocate, respondent, res_advocate])

    except TimeoutException:
        print("Timeout occurred while waiting for the elements to load.")

    finally:
        driver.switch_to.default_content()

# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

# Fxn to go back
def go_back(level):
    try:
        xpath = f'//a[@href="javascript:back({level})"]'
        back_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        back_button.click()
        scroll_down_500()
        time.sleep(3)
    except Exception as e:
        print(f"An error occurred while going back: {e}")

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
    # dfs = []

    # Iterate through each table row 
    table1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="example_year"]/tbody')))
    table1_rows = table1.find_elements(By.TAG_NAME, "tr")
    for row1 in table1_rows:
        print(row1.text)
        row1.find_element(By.XPATH, './td[4]/a').click()
        print('clicked table 1')
        time.sleep(2)

        # scroll the page
        scroll_down_500()

        # State Level 
        table2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="example_state"]/tbody')))
        table2_rows = table2.find_elements(By.TAG_NAME, "tr")
        # Iterate through each table row 
        for row2 in table2_rows:
            print(row2.text)
            row2.find_element(By.XPATH, './td[4]/a').click()
            print('clicked table 2')
            time.sleep(1)

            # scroll the page
            scroll_down_500()

            # District Level 
            table3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//tbody[@id="dist_report_body"]')))
            table3_rows = table3.find_elements(By.TAG_NAME, "tr")
            # Iterate through each table row 
            for row3 in table3_rows:
                print(row3.text)
                row3.find_element(By.XPATH, './td[4]/a').click()
                print('clicked table 3')
                time.sleep(1)

                # scroll the page
                scroll_down_500()   

                # Court Level
                wait = WebDriverWait(driver, 20)
                table4 = wait.until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='est_report_body']")))
                table4_rows = table4.find_elements(By.TAG_NAME, "tr")
                for row4 in table4_rows:
                    # Adding an explicit wait before clicking on the element
                    row4.find_element(By.XPATH, './td[4]/a').click()
                    print('Clicked table 4')

                    # time.sleep(15)

                    # Check if the directory exists, if not, create it
                    if not os.path.exists('CaptchaImg'):
                        os.makedirs('CaptchaImg')
                    
                    cathcha_solve_loop()
                    print("HELLO")

                    # # Process captcha multiple times
                    # for _ in range(15):
                    #     try:
                    #         process_captcha()

                    #         # submit button
                    #         submit_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')))
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

                    # print("HELLO")

                    # Cases
                    table5 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//tbody[@id="cases_report_body"]')))
                    table5_rows = table5.find_elements(By.TAG_NAME, "tr")
                    # Iterate through each table row 
                    for row5 in table5_rows:
                        print(row5.text)
                        row5.find_element(By.XPATH, './td/a').click()
                        print('clicked table 5')
                        time.sleep(1)
                        # scroll the page
                        scroll_down_500() 
                        time.sleep(20)

                        # Extract Case Information
                        scrape_case_details(driver)
                        
                        go_back(6)
                        print("back6")
                    go_back(4)  # Goes back 4 levels : cases table 
                    print("back4")
                
                go_back(3) # Goes back 3 levels : court level
                print("back3")

            go_back(2)  # Goes back 2 levels : district level
            print("back2")

        go_back(1)  # Goes back 1 level : state level
        print("back1")

        
finally:
    # Quit the WebDriver session
    driver.quit()

    # Concatenate all DataFrames in dfs list
    # final_df = pd.concat(dfs, ignore_index=True)

    # # Save to CSV
    # final_df.to_csv('cases.csv', index=False)
    # print("done csv")
    # print(final_df)