from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import time

app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)

# Function to verify if the user is already logged in
def verifyIfImLogin(driver):
    try:
        # Look for a specific element that indicates you are logged in.
        # Replace 'your_logged_in_element_id' with the actual ID or attribute of the element.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login_button'))
        )
        return True
    except:
        return False

# Function to automate the login
def automate_login(driver, usernameLogin, passwordLogin, email):
    # Check if already logged in
    if not verifyIfImLogin(driver):
        # Navigate to the website
        website_url = 'http://ky-iptv.com/HckqYJZU/login?referrer=logout'
        driver.get(website_url)

        # Locate the username and password input fields and submit button by their HTML attributes
        username_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login_button')

        # Enter username and password
        username_field.send_keys(usernameLogin)
        password_field.send_keys(passwordLogin)

        # Perform the login action (click the login button)
        login_button.click()
        time.sleep(10)
    #     return
    # else:
        # Navigate to the desired page
        # driver.get("http://ky-iptv.com/HckqYJZU/line")

        # # Locate the email input field and submit button
        # email_field = driver.find_element(By.ID, 'contact')
        # email_field.send_keys(email)

        # next_button = driver.find_element(By.XPATH, "//a[@href='javascript: void(0);']")
        # next_button.click()

        # # Locate and click the purchase button
        # purchase_button = driver.find_element(By.ID, 'submit_button')
        # purchase_button.click()

        # Navigate to the lines page
        driver.get("http://ky-iptv.com/HckqYJZU/lines")
        time.sleep(10)

        # Locate the last <tr> element within the <tbody> of the <table>
        last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")

        # Locate the first <td> element within the last <tr>
        username = last_tr.find_element(By.XPATH, ".//td[2]")
        password = last_tr.find_element(By.XPATH, ".//td[3]")

        # Get the username and password values
        username_text = username.text
        password_text = password.text
        print(f"username : {username_text} password : {password_text}")
        return username_text,password_text
    


# Define a Flask route for automation using GET method
@app.route('/getResult/<string:usernameLogin>/<string:passwordLogin>/<string:email>', methods=['GET'])
def getResult(usernameLogin,passwordLogin,email):
    # Retrieve data from query parameters
    # usernameLogin = request.args.get('usernameLogin')
    # passwordLogin = request.args.get('passwordLogin')
    # email = request.args.get('email')

    # Initialize the webdriver for Firefox
    driver = webdriver.Firefox()

    try:
        username_result, password_result = automate_login(driver, usernameLogin, passwordLogin, email)
        #print(f"{jsonify({'username': username_result, 'password': password_result})}")
         # Create a dictionary with the results
        result_dict = {"username": username_result, "password": password_result}
        print(f"{result_dict}")

        # Return the JSON response
        return result_dict
    finally:
        # Close the browser window
        driver.quit()
app.run()
