import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime
import pandas as pd
import os
from io import BytesIO
from PIL import Image
import pytesseract

# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment this line for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Fxn to capture and process captcha
def process_captcha():
    # Add synchronization and error handling as necessary
    image_element = driver.find_element(By.XPATH, "//img[@id='captcha_image1']")

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

    # Perform OCR on cropped image
    text = pytesseract.image_to_string(cropped_image)[:5]

    # Fill captcha input with extracted text
    captcha_input = driver.find_element(By.ID, "captcha1")
    time.sleep(2)
    captcha_input.clear()
    captcha_input.send_keys(text)

# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

current_datetime = datetime.now()  # Get the current date and time

url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'

# Main script
try:
    # Navigate to the webpage and perform necessary actions
    driver.get(url)
    driver.maximize_window()
    # Scroll the page
    scroll_down_500()

    element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
    # 600
    # Click on the element
    element.click()
    time.sleep(3)

    element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
    # 23 
    element1.click()
    time.sleep(3)

    element2 = driver.find_element(By.LINK_TEXT, "23")
    element2.click()
    time.sleep(3)

    element3 = driver.find_element(By.LINK_TEXT, "19")
    element3.click()
    time.sleep(3)

    # Scroll
    scroll_down_500()

    # Click the captcha link
    captcha_link = driver.find_element(By.XPATH, '//*[@id="est_report_body"]/tr[1]/td[4]/a')
    captcha_link.click()
    time.sleep(4)

    # Check if the directory exists, if not, create it
    if not os.path.exists('CaptchaImg'):
        os.makedirs('CaptchaImg')

    # Download Captcha img for solving
    # Process captcha multiple times
    for _ in range(15):
        process_captcha()
        
        # submit button
        submit_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')
        time.sleep(2)
        submit_button.click()
        time.sleep(5)
        print("Captcha processing completed.")
finally:
    # Quit the WebDriver session
    driver.quit()








