import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    
    driver = uc.Chrome()
    driver.get('https://accounts.google.com/')

    # add email
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys('YOUR EMAIL')
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
    sleep(3)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys('YOUR PASSWORD')
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
    sleep(10)
class Main:
  def __init_(self) -> None:
    self.url    = 'https://accounts.google.com/ServiceLogin'
    self.driver = driver = uc.Chrome(use_subprocess=True)
    self.time   = 10
    
  def login(self, email, password):
    # edit: fixed missing end-quotes on below lines
    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(f'{password}\n')
                                                                                
    self.code()
                                                                                  
  def code(self):
    # [ ---------- paste your code here ---------- ]
    time.sleep(self.time)                                                                                  
                                                                                  
if __name__ == "__main__":
  #  ---------- EDIT ----------
  email = 'email' # replace email
  password = 'password' # replace password
  #  ---------- EDIT ----------                                                                                                                                                         
 
  driver = Main()
  driver.login(email, password) 