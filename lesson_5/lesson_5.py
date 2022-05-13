from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import time
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_db']
mvideo = db.mvideo

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s)
driver.maximize_window()

driver.get("https://www.mvideo.ru/")

driver.execute_script("window.scrollTo(0, 1500);")
time.sleep(4)

try:
    driver.find_element(By.XPATH, "//mvid-shelf-group/*//span[contains(text(), 'В тренде')]").click()
except exceptions.NoSuchElementException:
    print('Not found')

items = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")

items_list = []

for item in items:
    item_info = {}
    item_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
    item_title = item.find_element(By.TAG_NAME, 'a').text

    item_info['title'] = item_title
    item_info['link'] = item_link

    items_list.append(item_info)

    try:
        mvideo.insert_one(item_info)
        mvideo.create_index('link', unique=True)
    except DuplicateKeyError:
        print(f'{item_info} is already exist')

driver.quit()

result = list(mvideo.find({}))
pprint(result)
print(f'Кол-во записей: {len(result)}')


