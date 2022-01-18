from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

chromedrive_path = 'C:/Users/flami/Downloads/chromedriver_win32' # use the path to the driver you downloaded from previous steps
driver = webdriver.Chrome()
# URL
url = 'https://www.google.com/maps/place/Arhaus/@32.7101066,-97.3996177,17z/data=!3m2!4b1!5s0x864e72f661d37209:0xb355a578738b526b!4m5!3m4!1s0x864e72f14da0106b:0x2ebd446b026677af!8m2!3d32.7102086!4d-97.3974338'
driver.get(url)

driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span/span[2]/span[1]/button').click()

#to make sure content is fully loaded we can use time.sleep() after navigating to each page

time.sleep(3)

total_number_of_reviews = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]').text.split(" ")[0]
total_number_of_reviews = int(total_number_of_reviews.replace(',','')) if ',' in total_number_of_reviews else int(total_number_of_reviews)
#Find scroll layout
scrollable_div = driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]')

#Scroll as many times as necessary to load all reviews
for i in range(0,(round(total_number_of_reviews/10 - 1))):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                scrollable_div)
        time.sleep(1)

response = BeautifulSoup(driver.page_source, 'html.parser')
reviews = response.find_all('div', class_='ODSEW-ShBeI NIyLF-haAclf gm2-body-2')

def get_review_summary(result_set):
    rev_dict = {'Review Rate': [],
        'Review Time': [],
        'Review Text' : []}
    for result in result_set:
        review_rate = result.find('span', class_='ODSEW-ShBeI-H1e3jb')["aria-label"]
        review_time = result.find('span',class_='ODSEW-ShBeI-RgZmSc-date').text
        review_text = result.find('span',class_='ODSEW-ShBeI-text').text
        rev_dict['Review Rate'].append(review_rate)
        rev_dict['Review Time'].append(review_time)
        rev_dict['Review Text'].append(review_text)
    return(pd.DataFrame(rev_dict))

df = get_review_summary(reviews)
df.to_csv('C:/Users/flami/Downloads/SGF/ARHS/Arhaus Reviews Fort Worth TX.csv')
print("Hello World")
