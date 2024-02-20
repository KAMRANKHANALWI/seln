from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time


website_url = 'https://njdg.ecourts.gov.in/njdgnew/?p=main/index&state_code=7~26'
chrome_driver_path = '/Users/kamrankhanalwi/Desktop/seln/chromedriver/chromedriver'

# instantiate a Service instance with the path
chrome_service = Service(chrome_driver_path)

# start the driver service
chrome_service.start()

# Pass the service object when creating the Chrome WebDriver instance
driver = webdriver.Chrome(service=chrome_service)

# Fxn to scroll the page 
def scroll_down_500():
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)

def scroll_down_1000():
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)


# open the website
driver.get(website_url)
driver.maximize_window()
# scroll the page
scroll_down_500()
# Choose 600 cases 
element = driver.find_element(By.XPATH, "//a[@href=\"javascript:fetchYearData('tot20_30',1)\"]")
element.click()
time.sleep(2)

# scroll the page
scroll_down_500() 

# Create an empty list to store DataFrames for each iteration
dfs = []

table1_rows = driver.find_elements(By.XPATH, '//table[@id="example_year"]/tbody/tr')
# Iterate through each table row 
for row in table1_rows:
    print(row.text)
    row.find_element(By.XPATH, './td[4]/a').click()
    # 23
    print('clicked table 1')
    time.sleep(1)

    # scroll the page
    scroll_down_500()

    # State Level 
    table2_rows = driver.find_elements(By.XPATH, '//table[@id="example_state"]/tbody/tr')
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
        table3_rows = driver.find_elements(By.XPATH, '//tbody[@id="dist_report_body"]/tr')
        # Iterate through each table row 
        for row in table3_rows:
            print(row.text)

            row.find_element(By.XPATH, './td[4]/a').click()
            # 14 
            print('clicked table 3')
            time.sleep(1)

            # scroll the page
            scroll_down_500()   

            # Court Level
            table4_rows = driver.find_elements(By.XPATH, "//tbody[@id='est_report_body']/tr")

            # Create an empty list to store Cases for each iteration
            Cases = []

            # Iterate through each table row 
            for row in table4_rows:
                # print(row.text)
                
                row.find_element(By.XPATH, './td[4]/a').click()
                print('clicked table 4')
                time.sleep(10)

                submit_button = driver.find_element(By.XPATH, '//input[@class="btn btn-success col-auto btn-sm"]')
                time.sleep(2)
                submit_button.click()
                time.sleep(5)

                scroll_down_500()

                cases_rows = driver.find_elements(By.XPATH, "//tbody[@id='cases_report_body']/tr")

                Cases = []

                # Iterate through each case table row 
                for row in cases_rows:
                    print(row.text)
                    cases = row.find_element(By.XPATH, './td[1]').text
                    Cases.append(cases)
                    print(cases)
                    # Cases.append(row.find_element(By.XPATH, './td[1]').text)
                    
                # back from cases table 
                back_4 = driver.find_element(By.XPATH, '//a[@href="javascript:back(4)"]')
                back_4.click()
                scroll_down_500()
                time.sleep(1)

            # Create DataFrame for each iteration and append to dfs list
            df = pd.DataFrame({'Cases': Cases})
            dfs.append(df)

            # back 3 from court level
            back_3 = driver.find_element(By.XPATH, '//a[@href="javascript:back(3)"]')
            back_3.click()
            scroll_down_500()
            time.sleep(1)

        # back 2 from district level
        back_2 = driver.find_element(By.XPATH, '//a[@href="javascript:back(2)"]')
        back_2.click()
        scroll_down_500()
        time.sleep(1)

    # back 1 from district level
    back_1 = driver.find_element(By.XPATH, '//a[@href="javascript:back(1)"]')
    back_1.click()
    scroll_down_500()
    time.sleep(1)


driver.quit()
chrome_service.stop()

# Concatenate all DataFrames in dfs list
final_df = pd.concat(dfs, ignore_index=True)

# Save to CSV
final_df.to_csv('cases.csv', index=False)
print("done csv")
print(final_df)