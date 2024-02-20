from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
from PIL import Image
import pytesseract

# Define the website URL and the path to the Chrome WebDriver
website_url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
chrome_driver_path = '/Users/kamrankhanalwi/Desktop/seln/chromedriver/chromedriver'

# Instantiate a Chrome Service instance with the specified path
chrome_service = Service(chrome_driver_path)

# Start the Chrome Driver service
chrome_service.start()

# Pass the service object when creating the Chrome WebDriver instance
driver = webdriver.Chrome(service=chrome_service)

# Open the specified website
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

# submit button
# time.sleep(40)
# submit_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')
# time.sleep(2)
# submit_button.click()
# time.sleep(5)

# Get the captcha image source
captcha_image_url = driver.find_element(By.ID, 'captcha_image1').get_attribute('src')

# Download the captcha image
captcha_image_data = requests.get(captcha_image_url).content

# Save the captcha image locally
with open('captcha_image.png', 'wb') as f:
    f.write(captcha_image_data)

# Use PyTesseract to extract text from the captcha image
captcha_text = pytesseract.image_to_string(Image.open('captcha_image.png'))
time.sleep(4)
print("Extracted Captcha Text:", captcha_text)

# Find the input field for the captcha
# captcha_input = driver.find_element(By.ID, 'captcha_input_id')  # Adjust the ID as per your HTML
captcha_input = driver.find_element(By.XPATH, '//*[@id="captcha1"]')

# Enter the extracted captcha text into the input field
captcha_input.send_keys(captcha_text)
time.sleep(5)



# Remember to stop the service when you're done with the driver
driver.quit()
chrome_service.stop()
