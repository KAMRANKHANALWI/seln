from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Define the website URL and the path to the Chrome WebDriver
website_url = 'https://www.adamchoi.co.uk/overs/detailed'
chrome_driver_path = '/Users/kamrankhanalwi/Desktop/seln/chromedriver/chromedriver'

# Instantiate a Chrome Service instance with the specified path
chrome_service = Service(chrome_driver_path)

# Start the Chrome Driver service
chrome_service.start()

# Pass the service object when creating the Chrome WebDriver instance
driver = webdriver.Chrome(service=chrome_service)

# Open the specified website
driver.get(website_url)

time.sleep(2)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

time.sleep(4)

matches = driver.find_elements(By.TAG_NAME, 'tr') 

date = []
home_team = []
score = []
away_team = []

for match in matches:
    # print(match.text)
    date.append(match.find_element(By.XPATH, './td[1]').text)
    # home_team.append(match.find_element(By.XPATH, './td[2]').text)
    home = match.find_element(By.XPATH, './td[2]').text
    home_team.append(home)
    print(home)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)


# Remember to stop the service when you're done with the driver
driver.quit()
chrome_service.stop()

# save to csv
df = pd.DataFrame({'date' : date, 'home_team' : home_team, 'score' : score, 'away_team' : away_team})
df.to_csv('football_data.csv', index=False)
print(df)