import re
import time
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException, ElementClickInterceptedException
from datetime import datetime
import csv
import os
from io import BytesIO
from PIL import Image
import pytesseract

# Firefox 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# # Chrome 
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
driver.get(url)
driver.maximize_window() 
driver.execute_script("window.scrollTo(0, 600);")
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

'''STEP 9 == Filling Captcha Image - 2 '''
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
            crop_image = (870, 670, 1100, 760)
            cropped_image = image.crop(crop_image) 
            cropped_image.save(img_download_path) 
            is_executed = True
        else:
            crop_image = (890, 540, 1100, 610)
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

        # '''STEP 11 == After Solving the Captcha Filling the data captcha data into input & Submit'''
        # # Fill captcha input with extracted text
        # captcha_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "captcha")))
        # captcha_input.clear()
        # captcha_input.send_keys(cleaned_text)
        # time.sleep(5)

        # # Submit Button 
        # xpath = '//input[@type="submit"]'
        # wait = WebDriverWait(driver, 20)  
        # element = wait.until(EC.presence_of_element_located((By.XPATH, xpath))) 
        # element.click() 

        # time.sleep(5)

        # try:
        #     element = driver.find_element(By.XPATH, '//span[@class="error"]')
        #     if element:
        #         print("errroooorr")
        #         continue
        # except:
        #     break

        # try:
        #     element = driver.find_element(By.XPATH, '//span[@class="error"]')
        #     if element:
        #         print("Error: An error element was found")
        #         # Do something here if needed
        # except NoSuchElementException:
        #     pass  # Continue the loop if no error element is found

        # # Navigate to the next page
        # # Add your code here to navigate to the next page

        # # Check for the presence of a certain element on the next page
        # try:
        #     wait = WebDriverWait(driver, 10)
        #     iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='case_history']")))
        #     driver.switch_to.frame(iframe)

        #     next_page_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="part1"]/div[1]/span[2]')))
        #     # next_page_element = driver.find_element(By.XPATH, '//*[@id="part1"]/div[1]/span[2]')
        #     if next_page_element:
        #         print("Element found on the next page. Breaking the loop.")
        #         break  # Break the loop if the element is found on the next page
        # except NoSuchElementException:
        #     pass  # Continue the loop if the element is not found on the next page




        

'''STEP 6 == Filling Captcha Image - 1 '''
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

        # petitioner and advocate
        span_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="Petitioner_Advocate_table"]')))
        span_content = span_element.text
        lines_p = span_content.split('\n\n')
        # print(lines_p)

        petitioner = lines_p[0].strip()  # Strip extra spaces
        pet_advocate = "- ".join(lines_p[1].split("- ")[1:]).strip()
        # print("Petitioner:", petitioner)
        # print("Advocate:", pet_advocate)

        # Respondent and Advocate
        respondent_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="Respondent_Advocate_table"]')))
        respondent_content = respondent_element.text
        lines_r = respondent_content.split('\n\n')
        print(lines_r)

        respondent = lines_r[0].strip()  
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
        
        time.sleep(2)
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