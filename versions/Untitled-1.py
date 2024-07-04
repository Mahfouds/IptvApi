# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
import random

# %%
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

# %%
def zity(driver,website,choice1,choice2):
    driver.get(website)
    btn=driver.find_element(By.XPATH,'/html/body/main/article/section/form/div[1]/div/div/div/fieldset/div/div/div['+str(choice1)+']/div/label/span[1]')
    btn.click()
    btn=driver.find_element(By.XPATH,'/html/body/main/article/section/form/div[1]/div/div/div/fieldset/div/div/div['+str(choice2)+']/div/label/span[1]')
    btn.click()
    btn=driver.find_element(By.XPATH,'/html/body/main/article/section/form/div[2]/button')
    btn.click()

# %%
def generate_random_number():
    while True:
        random_number = random.randint(1, 8)
        if random_number != 5:
            return random_number

# %%
zity(driver,'https://www.surveymonkey.com/r/679DMMR',5,generate_random_number())


