import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime

import pandas as pd
import os
from io import BytesIO
from PIL import Image
import pytesseract


# # Configure Chrome options for headless mode
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

current_datetime = datetime.now()  # Get the current date and time

url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'

# Open the specified website
driver.get(url)
driver.maximize_window()

# Scroll the page
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600
# Click on the element
element.click()
time.sleep(3)

element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
# 23 
element1.click()
time.sleep(4)

element2 = driver.find_element(By.LINK_TEXT, "23")
element2.click()
time.sleep(5)

element3 = driver.find_element(By.LINK_TEXT, "19")
element3.click()
time.sleep(6)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(3)

# Click the captcha link
captcha_link = driver.find_element(By.XPATH, '//*[@id="est_report_body"]/tr[1]/td[4]/a')
captcha_link.click()
time.sleep(4)

# submit button
# time.sleep(40)
# submit_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')
# time.sleep(2)
# submit_button.click()
# time.sleep(5)

#########Loop#########
# ''' STEP 5 == Clicking on 20-30 year Total link'''
# xpath = "(//tbody[@id='est_report_body']/tr/td[4]/a)[1]"
# wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
# element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # Wait until the element is present
# element.click()  # Click on the element
# time.sleep(3)

# Check if the directory exists, if not, create it
if not os.path.exists('CaptchaImg'):
    os.makedirs('CaptchaImg')

'''STEP 6 == Download Captcha img for solving'''
for _ in range(15):
    # Get current datetime for file naming
    current_datetime = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    img_download_path = f'CaptchaImg/{current_datetime}.png'

    # Find captcha image element
    time.sleep(2)
    image_element = driver.find_element(By.ID, 'captcha_image1')
    time.sleep(2)
    location = image_element.location
    print("Location:", location)
    size = image_element.size
    print("Size:", size)

    screenshot = driver.get_screenshot_as_png()     # Capture screenshot of entire browser window
    image = Image.open(BytesIO(screenshot))

    # Calculate coordinates for cropping
    left = location['x'] + 250
    print(left)
    top = location['y'] + 400
    print(top)
    right = left + size['width'] + 150
    print(right)
    bottom = top + size['height'] + 100
    print(bottom)

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(img_download_path)


    # Perform OCR on the cropped image
    text = pytesseract.image_to_string(cropped_image)[:5]
    print("Extracted Text:", text)

    # Fill captcha input with extracted text
    captcha_input = driver.find_element("id", "captcha1")
    captcha_input.clear()
    captcha_input.send_keys(text)
    time.sleep(3)


    # current_datetime = datetime.now()
    # current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
    # img_download_path = f'CaptchaImg/{current_datetime}.png'

    # image_element = driver.find_element(By.XPATH, "//img[@id='captcha_image1']")
    # location = image_element.location
    # print(location)
    # size = image_element.size
    # print(size)
    # screenshot = driver.get_screenshot_as_png()  # Capture the screenshot of the entire browser window
    # image = Image.open(BytesIO(screenshot))  # Use Pillow to open the screenshot and crop the desired area

    # image.save(img_download_path)

    # image = Image.open(BytesIO(screenshot))  # Use Pillow to open the screenshot and crop the desired area
    # left = location['x'] + 250
    # print(left)
    # top = location['y'] + 400
    # print(top)
    # right = left + size['width'] + 150
    # print(right)
    # bottom = top + size['height'] + 100
    # print(bottom)

    # cropped_image = image.crop((left, top, right, bottom))  # Crop the image to the specified area
    # cropped_image.save(img_download_path)  # Save the cropped image to a file
    # time.sleep(2)

    # # STEP 7 == Solving the Captcha img for solving
    # if img_download_path is not None:
    #     image_path = img_download_path
    #     image = Image.open(image_path)

    #     text = pytesseract.image_to_string(image)  # Perform OCR on the image
    #     text = text[:5]

    #     # Print the extracted text
    #     print("Extracted Text:")
    #     print(text)
    # else:
    #     print("Not Able to find")

    # # STEP 8 == After Solving the Captcha Filling the data captcha data into input & Submit
    # captcha_input = driver.find_element("id", "captcha1")
    # captcha_input.clear()
    # captcha_input.send_keys(text)
    # time.sleep(3)

    xpath = '//input[@class="btn btn-success col-auto btn-sm"]'
    wait = WebDriverWait(driver, 20)  # Adjust the timeout as needed
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # Wait until the element is present
    element.click()  # Click on the element
    time.sleep(3)
    popup_timeout = 10
    try:
        popup = WebDriverWait(driver, popup_timeout).until(EC.alert_is_present())
        popup.accept()
        time.sleep(3)
    except:
        print("No alert found within the specified timeout.")
        break

print("Okay")

time.sleep(20)
