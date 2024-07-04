from flask import Flask, jsonify, g,request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import waitress
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
#from werkzeug.urls import unquote
from flask_cors import CORS
import time
import atexit
import psutil
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)
#app.config["DRIVER_IS_OPEN"] = False

def is_firefox_open():
    # Iterate through all running processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            # Check if the process name contains 'firefox'
            if 'firefox' in process.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle exceptions that may occur during the iteration
            pass

    return False
# Initialize the webdriver for Firefox
def init_driver():
    
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
        # #driver = webdriver.Chrome(ChromeDriverManager().install())
        # chrome_options=webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        #driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        # driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        atexit.register(lambda: driver.quit())  # Register a function to quit the driver at exit
        return driver

def get_download_url(driver,id):
    try:
        # Locate the input element with the ID 'download_url'
        download_url_input = driver.find_element(By.ID, id)

        # Get the content (value) of the input element
        download_url_content = download_url_input.get_attribute('value')

        return download_url_content
    except:
        return None

# Define your function to get the username and password from the first row
def get_first_row_username_password(driver, usernamePos, passwordPos):
    try:
        # Locate the first <tr> element within the <tbody> of the <table>
        first_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")

        # Locate the <td> elements within the first <tr> based on their positions
        username = first_tr.find_elements(By.XPATH, f".//td[{usernamePos}]")
        password = first_tr.find_elements(By.XPATH, f".//td[{passwordPos}]")

        # Return the text of the found elements
        return username[0].text, password[0].text
    except NoSuchElementException as e:
        print(f"Error: {str(e)}")
        return None

def uncheck_checkbox_by_class_and_value(driver, class_name, value):
    try:
        # Find the checkbox element by class name and value attribute
        checkbox = driver.find_element(By.XPATH, f"//input[@class='{class_name}' and @value='{value}']")
        
        # Check if the checkbox is currently checked
        if checkbox.is_selected():
            # If it's checked, uncheck it
            checkbox.click()
        print("unchecked adult option succeess")
        return True
    except:
        print("unchecked adult option not success")
        return True

def select_option_by_value(driver, select_id, option_value):
    try:
        # Locate the <select> element
        select_element = driver.find_element(By.ID, select_id)

       # Execute JavaScript to select the option by setting the value
        bools = driver.execute_script(f'''
            var select = arguments[0];
            var optionValue = "{option_value}";

            // Check if the option with the given value exists
            var optionExists = false;
            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].value === optionValue) {{
                    optionExists = true;
                    break;
                }}
            }}

            if (optionExists) {{
                // Set the value of the <select> element to the desired option value
                select.value = optionValue;

                // Trigger a 'change' event to update the UI
                var event = new Event('change', {{bubbles: true}});
                select.dispatchEvent(event);
                return true;
            }} else {{
                return false;
            }}
        ''', select_element)

        return bools
    except:
        return False

def select_option_by_text(driver, select_id, option_text):
    try:
        # Locate the <select> element
        select_element = driver.find_element(By.ID, select_id)
        option_text=str(option_text).lower()
        # Execute JavaScript to select the option by text
        # Execute JavaScript to select the option by text
        bools = driver.execute_script(f'''
            var select = arguments[0];
            var optionText = "{option_text}";
            var bools = false;

            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].text.toLowerCase() === optionText) {{
                    select.selectedIndex = i;
                    select.dispatchEvent(new Event('change'));
                    bools = true;
                    return bools;
                }}
            }}
            return bools;
        ''', select_element)

        return bools
    except Exception as e:
        return False
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
def automate_login(driver, usernameLogin, passwordLogin,plan):
    try:
        # Check if already logged in
        #if not verifyIfImLogin(driver):
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
        time.sleep(5) #10
    except Exception as e:
        return jsonify({"error": str(e)})

def setValueOnInputId(id,value,driver):   
        try:
            # Find the input element by id
            input_element = driver.find_element(By.ID, id)

            # Get the current value attribute
            current_value = input_element.get_attribute("value")

            # Check if the current value is empty (or any other condition)
            if not current_value:
                # Set the default value "GZdDjqPrxb"
                input_element.send_keys(value)
        except Exception as e:
            return jsonify({"error": str(e)})
def complete_payment_retourne_credentiels(plan,driver,clientUsername,clientPassword=None):
    try:
    #return
        #else:
            #Navigate to the desired page
        #by_text=select_option_by_text(driver,"package","Paid Trial")
        # if "-" in plan:
        #     # Replace the hyphen with a space
        #     plan = plan.replace("-", " ")
        

        if not clientPassword == None:
            # Find the input element by id
            setValueOnInputId('password',clientPassword,driver)
            
        input_element = driver.find_element(By.ID, "username")
        # Clear the existing value
        input_element.clear()
        # Input the value "GZdDjqPrxb"
        input_element.send_keys(clientUsername)
        by_text=select_option_by_text(driver,"package",plan)
        print(plan)
        print(by_text)
        time.sleep(5) #10
        if by_text == True:
            # next_button = driver.find_element(By.XPATH, "//a[@href='javascript: void(0);']")
            # next_button.click()
            element = driver.find_element(By.XPATH, '//a[@href="#review-purchase" and @data-toggle="tab"]')
            # Click on the element
            element.click()
            time.sleep(7)#5

            by_class_and_value=uncheck_checkbox_by_class_and_value(driver,"big_checkbox","13")
            time.sleep(5) #15 s

            if by_class_and_value:
                
                # Locate and click the purchase button
                purchase_button = driver.find_element(By.ID, 'submit_button')
                purchase_button.click()
                time.sleep(5)

                # Navigate to the lines page
                driver.get("http://ky-iptv.com/HckqYJZU/lines")
                time.sleep(8)
                # Use a CSS selector to locate the button by the onclick attribute
                # Find the input element by id
                input_element = driver.find_element(By.ID, "user_search")

                # Clear the existing value
                input_element.clear()
                # Input the value "GZdDjqPrxb"
                input_element.send_keys(clientUsername)

                # Optionally, you can press the Tab key to move to the next element
                input_element.send_keys(Keys.TAB)
                time.sleep(5)

            
            # Locate the last <tr> element within the <tbody> of the <table>

                # Locate the last <tr> element within the <tbody> of the <table>
                last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")
                formatted_date=None
                if not last_tr.text.strip() == "No data available in table":

                    # Locate the first <td> element within the last <tr>
                    id = last_tr.find_element(By.XPATH, ".//td[1]")
                    username = last_tr.find_element(By.XPATH, ".//td[2]")
                    password = last_tr.find_element(By.XPATH, ".//td[3]")

                    print(f"id: {id.text} username : {username.text} and  password : {password.text}")
                    expiredDate=last_tr.find_element(By.XPATH, ".//td[10]")
                    #print(f"the expired date is {expiredDate.text}")
                    # expiredDatetext=expiredDate.text
                    # expiration_date = searchClient(driver,username)
                    parsed_date = datetime.strptime(str(expiredDate.text), "%Y-%m-%d\n%H:%M:%S")
                    formatted_date = parsed_date.strftime("%m/%d/%Y %H:%M:%S")
                    print(f"Username is {username} and formatted expired date is {formatted_date}")

                    time.sleep(5)
            # Use a CSS selector to locate the button by the onclick 
                        
                    button = driver.find_element(By.XPATH, '//*[@id="datatable-users"]/tbody/tr[1]/td[12]/div/button[2]')

                    # Click the button
                    button.click()
                    #time.sleep(2)
                    by_value=select_option_by_value(driver,"download_type","m3u_plus?output=hls")
                    time.sleep(5)

                    if by_value:
                        return get_download_url(driver,"download_url"),formatted_date
                    else:
                        return "m3u_plus not found",None
                else:
                    return "account created "+clientUsername+"but not returned","error"
                    
            else:
                return "adult cancled checkbox not found",None
        else:
                return plan+"plan not found",None
    except Exception as e:
        return "account may created "+clientUsername+" but not send it",None


def complete_payment_retourne_credentiels_renew(plan,driver,clientUsername,clientPassword):

    try:
        print(f"{plan},{clientUsername},{clientPassword}")
    #return
        #else:
            #Navigate to the desired page
        #by_text=select_option_by_text(driver,"package","Paid Trial")
        # if "-" in plan:
        #     # Replace the hyphen with a space
        #     plan = plan.replace("-", " ")
        # if not clientUsername == None:
        #     # Find the input element by id
        #     setValueOnInputId('username',clientUsername,driver)

        # if not clientPassword == None:
        #     # Find the input element by id
        #     setValueOnInputId('password',clientPassword,driver)
        #     time.sleep(2) #10

            
            
        by_text=select_option_by_text(driver,"package",plan)
        print(plan)
        print(by_text)
        time.sleep(5) #10
        if by_text == True:
            # next_button = driver.find_element(By.XPATH, "//a[@href='javascript: void(0);']")
            # next_button.click()
            #time.sleep(5) #10
            print("before prob")
            element = driver.find_element(By.XPATH, '//*[@id="basicwizard"]/ul/li[2]/a')
            # Click on the element
            element.click()
            time.sleep(7)#5
            print("after prob")

            by_class_and_value=uncheck_checkbox_by_class_and_value(driver,"big_checkbox","13")
            time.sleep(5) #15 s

            if by_class_and_value:
                
                # Locate and click the purchase button
                purchase_button = driver.find_element(By.ID, 'submit_button')
                purchase_button.click()
                time.sleep(5)

                # Navigate to the lines page
                driver.get("http://ky-iptv.com/HckqYJZU/lines")
                time.sleep(8)
                # Use a CSS selector to locate the button by the onclick attribute
                # Find the input element by id
                input_element = driver.find_element(By.ID, "user_search")

                # Clear the existing value
                input_element.clear()
                # Input the value "GZdDjqPrxb"
                input_element.send_keys(clientUsername)

                # Optionally, you can press the Tab key to move to the next element
                input_element.send_keys(Keys.TAB)
                time.sleep(5)

            
            # Locate the last <tr> element within the <tbody> of the <table>

                # Locate the last <tr> element within the <tbody> of the <table>
                last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")
                formatted_date=None
                if not last_tr.text.strip() == "No data available in table":

                    # Locate the first <td> element within the last <tr>
                    id = last_tr.find_element(By.XPATH, ".//td[1]")
                    username = last_tr.find_element(By.XPATH, ".//td[2]")
                    password = last_tr.find_element(By.XPATH, ".//td[3]")

                    print(f"id: {id.text} username : {username.text} and  password : {password.text}")
                    expiredDate=last_tr.find_element(By.XPATH, ".//td[10]")
                    #print(f"the expired date is {expiredDate.text}")
                    # expiredDatetext=expiredDate.text
                    # expiration_date = searchClient(driver,username)
                    parsed_date = datetime.strptime(str(expiredDate.text), "%Y-%m-%d\n%H:%M:%S")
                    formatted_date = parsed_date.strftime("%m/%d/%Y %H:%M:%S")
                    print(f"Username is {username} and formatted expired date is {formatted_date}")

                    time.sleep(5)
            # Use a CSS selector to locate the button by the onclick 
                        
                    button = driver.find_element(By.XPATH,'//*[@id="datatable-users"]/tbody/tr[1]/td[12]/div/button[2]')

                    # Click the button
                    button.click()
                    #time.sleep(2)
                    by_value=select_option_by_value(driver,"download_type","m3u_plus?output=hls")
                    time.sleep(5)

                    if by_value:
                        return get_download_url(driver,"download_url"),formatted_date
                    else:
                        return "m3u_plus not found",None
                else:
                    return "account created "+clientUsername+"but not returned","error"
            #   
                    
            else:
                return "adult cancled checkbox not found",None
        else:
                return plan+" not found",None
    except Exception as e:
                return "account may renewed "+clientUsername+" but not send it",None

# Define a Flask route for automation using GET method
@app.route('/getResult/<string:usernameLogin>/<string:passwordLogin>/<string:clientUsername>', methods=['POST'])
def getResult(usernameLogin, passwordLogin,clientUsername):
    try:
            # Optional parameter usernameClient is part of the route, but it's not require
        # Retrieve data from request payload (JSON)
        data = request.get_json()
        print(f"daat request in get result {data}")

        plan = data.get('plan')  # Assuming 'text' is the key in your payload
        usernameKoneo=data.get('koneo_login')
        pwdKoneo=data.get('koneo_pwd')
        merchantId=data.get('merchantId')
        merchantMail=data.get('merchantMail')
        print(f"in get resssssult before {usernameKoneo} and {merchantMail} nad {merchantId}")
        # Retrieve data from query parameters
        driver = g.driver  # Get the driver from the Flask global context
        isPaypalChanged=changePaypal(driver,usernameKoneo,pwdKoneo,merchantId,merchantMail)
        automate_login(driver, usernameLogin, passwordLogin,plan)

        #add
        driver.get("http://ky-iptv.com/HckqYJZU/lines")

        # Find the input element by id
        input_element = driver.find_element(By.ID, "user_search")

        # Clear the existing value
        input_element.clear()
        # Input the value "GZdDjqPrxb"
        input_element.send_keys(clientUsername)

        # Optionally, you can press the Tab key to move to the next element
        input_element.send_keys(Keys.TAB)
        time.sleep(5)

        result_dict=None

        # Locate the last <tr> element within the <tbody> of the <table>
        last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")
        if not last_tr.text.strip() == "No data available in table":
             # Locate the first <td> element within the last <tr>
            id = last_tr.find_element(By.XPATH, ".//td[1]")
            username = last_tr.find_element(By.XPATH, ".//td[2]")
            password = last_tr.find_element(By.XPATH, ".//td[3]")
            myPassword=password.text
            print(f"id: {id.text} username : {username.text} and  password : {password.text}")
            time.sleep(5)
            driver.get("http://ky-iptv.com/HckqYJZU/line?id="+id.text)
            print("hello after entre the renew form")
            time.sleep(15)
            print("password.txt"+myPassword)
            link,expiredDate=complete_payment_retourne_credentiels_renew(plan,driver,clientUsername,myPassword)
            expiredDate = "error" if not expiredDate else expiredDate
        
            # usernameKoneo=data.get('koneo_login')
            # pwdKoneo=data.get('koneo_pwd')
            # merchantId=data.get('merchantId')
            # merchantMail=data.get('merchantMail')
            # print(f"in getResult {usernameKoneo} and {merchantMail} nad {merchantId}")
            # isPaypalChanged=changePaypal(driver,usernameKoneo,pwdKoneo,merchantId,merchantMail)
            if isPaypalChanged :
                result_dict = {"link": link,"ready":"creation success","expiredDate":expiredDate}
            else:
                result_dict = {"link": link,"ready":"creation success but paypal not change it","expiredDate":expiredDate}


        else:

        #end add
            #automate_login(driver, usernameLogin, passwordLogin,plan)
            driver.get("http://ky-iptv.com/HckqYJZU/line")
            link,expiredDate = complete_payment_retourne_credentiels(plan,driver,clientUsername)
            expiredDate = "error" if not expiredDate else expiredDate
            result_dict = {"link": link,"ready":"created success","expiredDate":expiredDate}

        # Clean up and exit the driver
        cleanup_driver(driver)

        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": "error from generate account function"})
    
# Define a Flask route for automation using GET method
@app.route('/renew/<string:usernameLogin>/<string:passwordLogin>/<string:usernameClient>', methods=['POST'])
def renew(usernameLogin, passwordLogin, usernameClient):
    try:
        data = request.get_json()
        print(f"daat request in renew {data}")
        plan = data.get('plan') 
        usernameKoneo=data.get('koneo_login')
        pwdKoneo=data.get('koneo_pwd')
        merchantId=data.get('merchantId')
        merchantMail=data.get('merchantMail')
        print(f"in renew before {usernameKoneo} and {merchantMail} nad {merchantId}")

        driver = g.driver
        # website_url = 'http://ky-iptv.com/HckqYJZU/login?referrer=logout'
        # driver.get(website_url)
        isPaypalChanged=changePaypal(driver,usernameKoneo,pwdKoneo,merchantId,merchantMail)

        automate_login(driver, usernameLogin, passwordLogin,plan)

        driver.get("http://ky-iptv.com/HckqYJZU/lines")

        # Find the input element by id
        input_element = driver.find_element(By.ID, "user_search")

        # Clear the existing value
        input_element.clear()
        # Input the value "GZdDjqPrxb"
        input_element.send_keys(usernameClient)

        # Optionally, you can press the Tab key to move to the next element
        input_element.send_keys(Keys.TAB)
        time.sleep(5)

        result_dict=None

        # Locate the last <tr> element within the <tbody> of the <table>
        last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")
        if not last_tr.text.strip() == "No data available in table":

            # Locate the first <td> element within the last <tr>
            id = last_tr.find_element(By.XPATH, ".//td[1]")
            username = last_tr.find_element(By.XPATH, ".//td[2]")
            password = last_tr.find_element(By.XPATH, ".//td[3]")
            myPassword=password.text
            print(f"id: {id.text} username : {username.text} and  password : {password.text}")
            time.sleep(5)
            driver.get("http://ky-iptv.com/HckqYJZU/line?id="+id.text)
            print("hello after entre the renew form")
            time.sleep(15)
            print("password.txt"+myPassword)
            link,expiredDate=complete_payment_retourne_credentiels_renew(plan,driver,usernameClient,myPassword)
            expiredDate = "error" if not expiredDate else expiredDate
        
            print(f"in renew {usernameKoneo} and {merchantMail} nad {merchantId}")
            # isPaypalChanged=changePaypal(driver,usernameKoneo,pwdKoneo,merchantId,merchantMail)
            if isPaypalChanged :
                result_dict = {"link": link,"ready":"renew success","expiredDate":expiredDate}
            else:
                result_dict = {"link": link,"ready":"renew success but paypal not change it","expiredDate":expiredDate}

                #link=complete_payment_retourne_credentiels(plan,driver)
                #result_dict = {"link": link}
                # print("expired")
            # else:
            #     print("not expired")
            #     result_dict = {"link": "the account not expired","ready":"renew not authorize"}
            #edit_package(plan,driver)
            

            # # Clean up and exit the driver
            # cleanup_driver(driver)  
        else:
            print("there is no result")
            #getResultWithoutRoute(usernameLogin, passwordLogin,usernameClient)
            result_dict = {"link": "can't find this user","ready":"renew failed"}

            # # Clean up and exit the driver
            # cleanup_driver(driver)
        # Clean up and exit the driver
            
        cleanup_driver(driver)
        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": "error from renew function"})

def expiredDate(driver,id):
    # Find the input element by id
    expDate = driver.find_element(By.ID, id)

    # Get the current value attribute
    expDateValue = expDate.get_attribute("value")

    # Convert the date string to a datetime object
    expDateDatetime = datetime.strptime(expDateValue, "%m/%d/%Y %H:%M:%S")  # Adjust the format based on your date input

    # Get the current date
    currentDate = datetime.now()

    # Compare the dates
    return expDateDatetime < currentDate  
def getResultWithoutRoute(usernameLogin, passwordLogin,usernameClient):
    try:
            # Optional parameter usernameClient is part of the route, but it's not require
        # Retrieve data from request payload (JSON)
        data = request.get_json()
        plan = data.get('plan')  # Assuming 'text' is the key in your payload
        # Retrieve data from query parameters
        driver = g.driver  # Get the driver from the Flask global context
        # automate_login(driver, usernameLogin, passwordLogin,plan)
        driver.get("http://ky-iptv.com/HckqYJZU/line")
        link = complete_payment_retourne_credentiels(plan,driver,usernameClient)
        expiredDate = "error" if not expiredDate else expiredDate
        
        result_dict = {"link": link,"expiredDate":expiredDate}
    

        # Clean up and exit the driver
        cleanup_driver(driver)

        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": str(e)})
    
def changePaypal(driver,username,password,merchantId,merchantMail):
    try : 
        # URL of the website you want to open and login to
        website_url = 'https://www.kooneo.com/'
        # username = 'shmahfoud74@gmail.com'
        # password = 'PPpp09@#'
        # Navigate to the website
        driver.get(website_url)
        refuseCookie=driver.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/button[1]')
        refuseCookie.click()
        time.sleep(5)
        seConnecterBtn=driver.find_element(By.XPATH,'/html/body/div/header/div[2]/a[2]')
        seConnecterBtn.click()
        usernameInput=driver.find_element(By.ID,'username')
        usernameInput.clear()
        usernameInput.send_keys(username)
        passwordInput=driver.find_element(By.ID,'password')
        passwordInput.clear()
        passwordInput.send_keys(password)
        loginBtn=driver.find_element(By.XPATH,'/html/body/div/main/div/div/div[2]/form/div/div[4]/div[1]/button')
        loginBtn.click()
        time.sleep(5)
        productsTab=driver.find_element(By.XPATH,'//*[@id="koo_btn_product"]')
        productsTab.click()
        time.sleep(5)
        modePaimentBtn=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/ul/li[9]')
        modePaimentBtn.click()
        time.sleep(5)
        current_url = driver.current_url
        print("Current URL:", current_url)
        url_parts = current_url.split("/")
        desired_part = "/".join(url_parts[3:5])  # Join parts 3 and 4 with "/"
        print("Desired part:", desired_part)
        driver.get("https://www.kooneo.com/"+desired_part+"/paymode/edit/3")
        time.sleep(5)
        # merchantId='5DC5PVVW83JJW'
        # merchantMail='shmahfoud74@gmail.com'
        time.sleep(5)
        merchantIdInput=driver.find_element(By.NAME,'idmarchand')
        merchantIdInput.clear()
        merchantIdInput.send_keys(merchantId)
        merchantMailInput=driver.find_element(By.NAME,'idvendeur')
        merchantMailInput.clear()
        merchantMailInput.send_keys(merchantMail)
        time.sleep(5)
        registerBtn=driver.find_element(By.CSS_SELECTOR,'#form-toolbox-btns button')
        registerBtn.click()
        time.sleep(5)
        return True
    except Exception as e:
        print("An error occurred:", str(e))
        return False

from threading import Lock

lock = Lock()
processed_requests = set()

@app.before_request
def before_request():
    global processed_requests
    current_params = (request.method, request.path, request.args)  # Capture current request parameters
    
    if not lock.locked():  # Check if the lock is not acquired
        lock.acquire()  # Acquire the lock
        print("the driver is open : " + str(is_firefox_open()))
        
        # Check if the current parameters match any of the processed requests
        if current_params in processed_requests:
            lock.release()  # Release the lock
            return "Duplicate request. Skipping processing.", 409
        
        if 'driver' not in g:
            g.driver = init_driver()  # Initialize the driver if it doesn't exist in the context
        
        processed_requests.add(current_params)  # Add current request parameters to processed requests
        lock.release()  # Release the lock
    else:
        # Do something here to handle the case where a request is already running
        return "Another request is already in progress. Please try again later.", 409

@app.after_request
def after_request(response):
    # Remove current request parameters from processed requests after responding to the request
    current_params = (request.method, request.path, request.args)
    processed_requests.discard(current_params)
    return response


        
# if __name__ == '__main__':
#     # Use Waitress to serve the Flask app
#     waitress.serve(app, host='0.0.0.0', port=5000)

# Function to clean up and exit the driver
def cleanup_driver(driver):
    try:
       
            driver.quit()
        

        
    except Exception as e:
        print(f"Error while cleaning up the driver: {e}")

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run()




