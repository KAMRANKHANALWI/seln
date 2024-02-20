import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
from PIL import Image
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
# scroll the page
driver.execute_script("window.scrollBy(0, 500);")

time.sleep(2)

element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# 600 cases 
element.click()
time.sleep(2)

# scroll 
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)  

element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
element1.click()
time.sleep(2)

# scroll the page
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

element2 = driver.find_element(By.LINK_TEXT, "23")
element2.click()
time.sleep(2)

element3 = driver.find_element(By.LINK_TEXT, "19")
element3.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)    

# Click the captcha link
element3 = driver.find_element(By.XPATH, '//*[@id="est_report_body"]/tr[1]/td[4]/a')
element3.click()
time.sleep(2)

# Scroll down by 500 pixels using JavaScript
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)
# captcha 1
time.sleep(15)

# Click the cases table link
element3 = driver.find_element(By.XPATH, '//tbody[@id="cases_report_body"]/tr/td/a')
element3.click()
time.sleep(20)



# # Find all span elements with class 'case_details_table' using XPath
# # case_details = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//span[@class="case_details_table"]')))
# case_details = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, '//span[@class="case_details_table"]')))

# # Initialize a dictionary to store case details
# case_details_dict = {}

# # Extract case details
# for detail in case_details:
#    label = WebDriverWait(driver, 10).until(
#    EC.presence_of_element_located((By.XPATH, './/label'))).text.strip()
#    # label = detail.find_element(By.XPATH, './/label').text.strip()
#    value = detail.text.split(':')[-1].strip()
#    case_details_dict[label] = value

   
# # Print case status details
#    for key, value in case_details_dict.items():
#       print(f"{key}: {value}")
   
# # Write data to a CSV file
# with open('case_details.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(['Key', 'Value'])  # Writing the header row
#    for key, value in case_details_dict.items():
#       writer.writerow([key, value])  # Writing each key-value pair

# print("Data saved to case_details.csv")

# Define data elements and their XPaths
data_elements = {
   # "Case Type": (By.XPATH, "//span[@class='case_details_table'][1]"),
   "Case Type": (By.XPATH, '//*[@id="part1"]/div[1]/span[2]'),
   "Filing Number": (By.XPATH, "//span[@class='case_details_table'][2]//span[1]"),
   "Filing Date": (By.XPATH, "//span[@class='case_details_table'][2]//span[2]"),
   "Registration Number": (By.XPATH, "//span[@class='case_details_table'][3]//span[1]"),
   "Registration Date": (By.XPATH, "//span[@class='case_details_table'][3]//span[2]"),
   "CNR Number": (By.XPATH, '//*[@id="part1"]/div[1]/b/span')
}

# Extract data and store in a dictionary
extracted_data = {}
for key, value in data_elements.items():
   element = driver.find_element(*value)
   extracted_data[key] = element.text

# Write extracted data to a CSV file
csv_file_path = 'extracted_data.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
   writer = csv.writer(csvfile)
   writer.writerow(['Field', 'Value'])
   for key, value in extracted_data.items():
      writer.writerow([key, value])


time.sleep(7)

driver.quit()
chrome_service.stop()

print(f"Data saved to {csv_file_path}")

# import csv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time

# # Define the website URL and the path to the Chrome WebDriver
# website_url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
# chrome_driver_path = '/Users/kamrankhanalwi/Desktop/seln/chromedriver/chromedriver'

# # Instantiate a Chrome Service instance with the specified path
# chrome_service = Service(chrome_driver_path)

# # Start the Chrome Driver service
# chrome_service.start()

# # Pass the service object when creating the Chrome WebDriver instance
# driver = webdriver.Chrome(service=chrome_service)

# # Open the specified website
# driver.get(website_url)
# driver.maximize_window()

# # Wait for the page to load
# time.sleep(5)

# # Scroll the page
# driver.execute_script("window.scrollBy(0, 500);")

# # Click on the necessary elements to reach the case details
# element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
# element.click()
# time.sleep(2)

# element1 = driver.find_element(By.XPATH, "//td/a[@href=\"javascript:fetchData('20 to 30 Years','tot20_30','1','1994')\"]")
# element1.click()
# time.sleep(2)

# element2 = driver.find_element(By.LINK_TEXT, "23")
# element2.click()
# time.sleep(2)

# element3 = driver.find_element(By.LINK_TEXT, "19")
# element3.click()
# time.sleep(2)

# # Scroll down the page
# driver.execute_script("window.scrollBy(0, 500);")
# time.sleep(2)

# # Click the captcha link
# element3 = driver.find_element(By.XPATH, '//*[@id="est_report_body"]/tr[1]/td[4]/a')
# element3.click()
# time.sleep(2)

# # Scroll down the page
# driver.execute_script("window.scrollBy(0, 500);")
# time.sleep(2)

# # Perform captcha solving process (Not included in the code)
# # captcha 1
# time.sleep(15)

# # Click the cases table link
# element3 = driver.find_element(By.XPATH, '//tbody[@id="cases_report_body"]/tr/td/a')
# element3.click()
# time.sleep(20)

# # Extract the HTML content of the page after clicking on the cases table link
# html_content = driver.page_source

# # Use BeautifulSoup to parse the HTML content
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find all span elements with class 'case_details_table'
# case_details = soup.find_all('span', class_='case_details_table')

# # Initialize a dictionary to store case details
# case_details_dict = {}

# # Extract case details
# for detail in case_details:
#    label = detail.find('label').text.strip()
#    value = detail.text.split(':')[-1].strip()
#    case_details_dict[label] = value

# # # Write data to a CSV file
# # with open('case_details.csv', 'w', newline='') as csvfile:
# #    writer = csv.writer(csvfile)
# #    writer.writerow(['Key', 'Value'])  # Writing the header row
# #    for key, value in case_details_dict.items():
# #       writer.writerow([key, value])  # Writing each key-value pair

# # print("Data saved to case_details.csv")
   
# # Print case status details
#    for key, value in case_details_dict.items():
#       print(f"{key}: {value}")


# # Write to CSV
# with open("case_details.csv", "w") as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow(case_details_dict.keys())
#    writer.writerow(case_details_dict.values())

# print("Data saved to case_details.csv")

# # Quit the WebDriver and stop the Chrome service
# driver.quit()
# chrome_service.stop()
