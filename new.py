from io import BytesIO
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from PIL import Image
import pyautogui
import pytesseract

# Firefox 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# # Chrome 
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

website_url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
driver.get(website_url)
driver.maximize_window()

# Scroll the page
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)
driver.execute_script("window.scrollBy(0, 100);")

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600
# Click on the element
element.click()
time.sleep(3)

element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
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

for _ in range(20):
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        img_download_path = f'CaptchaImg/{current_datetime}.png'



        # Wait for the captcha image to become visible
        image_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="captcha_image1"]')))

        # Get the size and location of the captcha element
        location = image_element.location
        size = image_element.size

        # Take a screenshot of the entire page
        screenshot = driver.get_screenshot_as_png()

        # Use PIL to open the screenshot
        image = Image.open(BytesIO(screenshot))

        # Calculate the region to crop
        left = location['x'] + 250  
        top = location['y'] + 400
        right = left + size['width'] + 150
        bottom = top + size['height'] + 100

        # Crop the image to the captcha region
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(img_download_path) # Save the cropped image to a file
        time.sleep(2)  # Just for stability


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
        captcha_input = driver.find_element("id", "captcha1")
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



# Remember to stop the service when you're done with the driver
driver.quit()
