import csv
import time
from selenium import webdriver
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


# # Firefox 
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# Chrome 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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

def cathcha2_solve_loop():
    # iframe = driver.find_element(By.XPATH,'//iframe[@id="case_history"]')
    # driver.switch_to.frame(iframe)
    is_executed = False
    for _ in range(15):
        iframe = driver.find_element(By.XPATH,'//iframe[@id="case_history"]')
        driver.switch_to.frame(iframe)
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 300);")
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
        # Save screenshot to a file
        with open('/Users/kamrankhanalwi/Desktop/seln/Captcha2Img/screenshot.png', 'wb') as f:
            f.write(screenshot)

        left = location['x']  
        top = location['y']
        right = left + size['width'] 
        bottom = top + size['height'] 

        # cropped_image = image.crop((left, top, right, bottom)) 
        if not is_executed:
            # crop_image = (870, 1240, 1100, 1300)
            # crop_image = (870, 1010, 1100, 1070)
            # crop_image = (870, 1230, 1100, 1320)
            # crop_image = (870, 670, 1100, 760)
            # crop_image = (870, 430, 1100, 520)
            crop_image = (870, 400, 1100, 480)
            cropped_image = image.crop(crop_image) 
            cropped_image.save(img_download_path) 
            is_executed = True
        else:
            # crop_image = (890, 540, 1100, 610)
            crop_image = (870, 430, 1100, 520)
            cropped_image = image.crop(crop_image) 
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
            print(cleaned_text)
            if cleaned_text ==  "":
                cleaned_text = '123'
            # print("Extracted Text:", cleaned_text)
        else:
            print("Not Able to find")

        # Captcha Input 
        captcha_input = driver.find_element("id", "captcha")
        captcha_input.clear()
        captcha_input.send_keys(cleaned_text)
        time.sleep(2)
        
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'guestlogin')))
        button.click()

        time.sleep(5)

        try:
            element = driver.find_element(By.XPATH, '//span[@class="error"]')
            if element:
                continue
        except:
            driver.switch_to.default_content()
            break
        

'''STEP  == Filling Captcha Image - 1 '''
def cathcha1_solve_loop():
    is_executed = False
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
        # Save screenshot to a file
        # with open('/Users/kamrankhanalwi/Desktop/seln/Captcha1Img/screenshot.png', 'wb') as f:
        #     f.write(screenshot)
        # Calculate cropping coordinates
        # left = location['x']
        # top = location['y']
        # right = left + size['width']
        # bottom = top + size['height']

        # cropped_image = image.crop((left, top, right, bottom))
        if not is_executed:
            crop_image = (480, 1020, 700, 1100)
            cropped_image = image.crop(crop_image)
            cropped_image.save(img_download_path) 
            is_executed = True
        else:
            crop_image = (480, 1080, 700, 1150)
            cropped_image = image.crop(crop_image)
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
        # Wait for the presence of the iframe with a timeout of 10 seconds
        wait = WebDriverWait(driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))

        # Switch to the iframe
        driver.switch_to.frame(iframe)

        wait = WebDriverWait(driver, 10)
        courtName_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[@class="h1class"]/span')))
        courtName = courtName_element.text
        print(courtName)
        case_type_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[2]')))
        case_type = case_type_element.text.split(":")[-1].strip()
        print(case_type)

        # filing_number 
        filing_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]')))
        filing_number = filing_number_element.text.split(":")[-1].strip()
        print(filing_number)


        # # filing_number 
        # filing_number_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]')))
        # text_content = filing_number_element.text

        # # Use regular expression to extract the desired pattern
        # pattern = r'\b\d{1,6}/\d{4}\b'
        # matches = re.findall(pattern, text_content)

        # # Initialize filing_number with a default value
        # filing_number = "Filing number not found"

        # if matches:
        #     filing_number = matches[0]
        #     print(filing_number)
        # else:
        #     print("Filing number not found")

        
        filing_date_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[3]/span[2]')))
        filing_date = filing_date_element.text.split(":")[-1].strip()
        file_day, file_month, file_year = parse_date_string(filing_date)
        print(filing_date)
        print(file_day)
        print(file_month)
        print(file_year)

        # try:
        #     # Locate the element containing filing information using XPath
        #     filing_number_element = driver.find_element(By.XPATH, "(//span[@class='case_details_table'])[2]")
        #     # Get the text content of the located element
        #     filing_info_text = filing_number_element.text
        #     # Print the original filing number information
        #     # print("Original Filing Information:", filing_info_text)
        #     # Use regular expression to extract the filing number
        #     filing_number_match = re.search(r'Filing\s*Number\s*:\s*(\d+/\d+)', filing_info_text)
        #     # Check if a match is found
        #     if filing_number_match:
        #         filing_number = filing_number_match.group(1).lstrip()
        #         # print("Extracted Filing Number:", filing_number)
        #         return filing_number
        #     else:
        #         print("Filing number not found.")

            
        # except Exception as e:
        #     print(f"An error occurred while fetching Filling Number: {str(e)}")
        #     return None

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
        firstDateSrt = ":".join(firstDate_element.text.strip().split(":")[1:4]).strip()
        print(firstDateSrt)
        firstDate = format_date_string(firstDateSrt)
        f_day, f_month, f_year = format_date(firstDateSrt)
        # print(firstDate)
        print(f_day)
        print(f_month)
        print(f_year)
        nextDate_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="part1"]/div[2]/span[2]/label/strong[2]')))
        # nextDateStr = ":".join(nextDate_element.text.strip().split(":")[1:4]).strip()
        # print(nextDateStr)
        
        # Extract the text content of the element
        nextDateStr = nextDate_element.text.strip()

        # Use regular expressions to extract the date pattern
        date_pattern = re.search(r'\d{1,2}\w{2} \w+ \d{4}', nextDateStr).group()

        print(date_pattern)

        nextDate = format_date_string(date_pattern)
        n_day, n_month, n_year = format_date(date_pattern)
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

    finally:
        driver.switch_to.default_content()

def back():
    backButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@id="iframe_back"]')))
    backButton.click()

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


    # Iterate through each table row 
    table1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@id="example_year"]/tbody')))
    # table1_rows = table1.find_elements(By.TAG_NAME, "tr")
    table1_rows = table1.find_elements(By.TAG_NAME, "tr")[4:]  # Exclude the first element
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
            table3_rows = table3.find_elements(By.TAG_NAME, "tr")[1:] 
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
                    time.sleep(2)
                    cathcha1_solve_loop()
                    print("CAPTCHA 1 HERE")

                    # Cases
                    table5 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//tbody[@id="cases_report_body"]')))
                    # table5_rows = table5.find_elements(By.TAG_NAME, "tr")
                    table5_rows = table5.find_elements(By.TAG_NAME, "tr")
                    # Iterate through each table row 
                    for row5 in table5_rows:
                        print(row5.text)
                        row5.find_element(By.XPATH, './td/a').click()
                        print('clicked table 5')
                        time.sleep(1)
                        # scroll the page
                        scroll_down_500() 
                        time.sleep(5)
                        print("CAPTCHA 2 HERE")
                        # cathcha2_solve_loop()
                        time.sleep(17)
                        # Extract Case Information
                        extract_text_loop(driver)
                        time.sleep(4)
                        # go_back(6)
                        back()
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
