from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import configparser
import config_file_read
import os
import os.path
from csv import writer

# Scrapes apartments daily (new apartments only within the last 24 hours)
#saves to csv file


if os.path.exists('info.ini'):
    d = input("Would you like to use the same housing information as last time?(y/n): ")
    if d == "n" or d == "N":
        config_file_read.write()

parser = configparser.ConfigParser()
config_file_read.read(parser)

House_type = parser.get("Details","type")
House_type = House_type.split(",")
House_type = [x.lower().replace(" ","") for x in House_type]

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.apartments.com/")
Location = parser.get("Location","city") + ", " + parser.get("Location","state")
try:
    Area = driver.find_element(By.ID,"quickSearchLookup")
    Area.send_keys(Location)
    Search = driver.find_element(By.LINK_TEXT,"Search")
    time.sleep(3)
    Search.click()
    Price = WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.ID,"rentRangeLink"))
    )
    Price.click()
    min_price = WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.ID,"min-input"))
    )
    min_price.send_keys(parser.get("Details","min"))
    max_price = WebDriverWait(driver,15).until(
        EC.presence_of_element_located((By.ID,"max-input"))
    )
    max_price.send_keys(parser.get("Details","max"))
    max_price.send_keys(Keys.RETURN)
    time.sleep(1)
    beds = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.ID,"bedRangeLink"))
    )
    beds.click()
    time.sleep(2)
    min_beds = int((parser.get("Details","beds")))
    min_beds += 1
    min_beds = str(min_beds)
    amount_of_beds = "/html/body/div[1]/main/section/header/div/span[3]/div/div/ul[1]/li[" + min_beds + "]"
    min_beds = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.XPATH,amount_of_beds))
    )
    min_beds.click()
    time.sleep(0.5)
    max_beds = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/main/section/header/div/span[3]/div/div/ul[2]/li[1]"))
    )
    max_beds.click()
    time.sleep(1)
    Type = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.ID,"typeSelect"))
    )
    Type.click()
    time.sleep(0.5)
    d = {"apartments":"0","houses":"1","condos":"2","townhomes":"3"}
    for word in House_type:
        if word in d.keys():
            Type = WebDriverWait(driver,15).until( 
                EC.presence_of_element_located((By.XPATH,'//*[@id="' + d[word] + '"]'))
            )
            Type.click()
            time.sleep(1)
    Type = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.ID,"typeSelect"))
    )
    Type.click()
    time.sleep(1)
    New = WebDriverWait(driver,15).until( 
        EC.presence_of_element_located((By.ID,"mapPillNewBtn"))
    )
    New.click()
    #include information of each house in csv file: address, price, amount of rooms
except:
    driver.quit()
time.sleep(5)

# check if the beds are either under "bed-range" or "property-beds". DO THE SAME FOR pricing
placards = driver.find_elements(By.CLASS_NAME,"placard")
House_names = driver.find_elements(By.CLASS_NAME,"property-address")
House_prices = driver.find_elements(By.CLASS_NAME,"price-range")
House_beds = driver.find_elements(By.CLASS_NAME,"bed-range")
House_beds2 = driver.find_elements(By.CLASS_NAME,"property-beds")
House_prices2 = driver.find_elements(By.CLASS_NAME,"property-pricing")
House_link = driver.find_elements(By.CLASS_NAME,"property-link")
url = list()
names = list()
for name in House_names: #loop ensures that there every adress must start with a number
    if name.text[0].isnumeric():
        names.append(name.text)

    for placard in placards:
        url.append(placard.get_attribute('data-url'))
with open('househunt.csv',mode='w') as f:
    write = writer(f)
    Header = ['Address','Price','Beds/Bathrooms','url']
    write.writerow(Header)

    for name, price, beds, link in zip(names,House_prices,House_beds,url):
        row = [name, price.text, beds.text, link]
        write.writerow(row)
    for name, price, beds,link in zip(House_names,House_prices2,House_beds2,url):
        row = [name, price.text, beds.text, link]
        write.writerow(row)

# to do: maybe figure out how to scroll and get next page?