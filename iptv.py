from flask import Flask, jsonify, g
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from flask_cors import CORS
import time
import atexit

app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)

# Initialize the webdriver for Firefox
def init_driver():
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()).options=chrome_options)
   
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
        print("unchecked succeess")
        return True
    except:
        print("unchecked not success")
        return False

def select_option_by_value(driver, select_id, option_value):
    try:
        # Locate the <select> element
        select_element = driver.find_element(By.ID, select_id)

        # Execute JavaScript to select the option by setting the value
        driver.execute_script(f'''
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

        return True
    except:
        return False

def select_option_by_text(driver, select_id, option_text):
    try:
        # Locate the <select> element
        select_element = driver.find_element(By.ID, select_id)

        # Execute JavaScript to select the option by text
        driver.execute_script(f'''
            var select = arguments[0];
            var optionText = "{option_text}";

            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].text.includes(optionText)) {{
                    select.selectedIndex = i;
                    select.dispatchEvent(new Event('change'));
                    return true;
                }}
            }}
            return false;
        ''', select_element)

        return True
    except:
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
def automate_login(driver, usernameLogin, passwordLogin):
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
    time.sleep(10)
    #return
    #else:
        #Navigate to the desired page
    driver.get("http://ky-iptv.com/HckqYJZU/line")

    by_text=select_option_by_text(driver,"package","Paid Trial")
    time.sleep(10)

    if by_text:
        next_button = driver.find_element(By.XPATH, "//a[@href='javascript: void(0);']")
        next_button.click()
        time.sleep(5)

        by_class_and_value=uncheck_checkbox_by_class_and_value(driver,"big_checkbox","13")
        time.sleep(15)

        if by_class_and_value:
            
            # Locate and click the purchase button
            purchase_button = driver.find_element(By.ID, 'submit_button')
            purchase_button.click()
            time.sleep(5)

            # Navigate to the lines page
            driver.get("http://ky-iptv.com/HckqYJZU/lines")
            time.sleep(5)
            # Use a CSS selector to locate the button by the onclick attribute
           
           # Locate the last <tr> element within the <tbody> of the <table>
            last_tr = driver.find_element(By.XPATH, "//table/tbody/tr[1]")

            # Locate the first <td> element within the last <tr>
            username = last_tr.find_element(By.XPATH, ".//td[2]")
            password = last_tr.find_element(By.XPATH, ".//td[3]")
           # Use a CSS selector to locate the button by the onclick attribute
            button = driver.find_element(By.CSS_SELECTOR, "[onclick*=\"download('"+username.text+"', '"+password.text+"');\"]")

            # Click the button
            button.click()
            by_value=select_option_by_value(driver,"download_type","m3u_plus?output=hls")
            time.sleep(5)

            if by_value:
                return get_download_url(driver,"download_url")
    return False
       
    


# Define a Flask route for automation using GET method
@app.route('/getResult/<string:usernameLogin>/<string:passwordLogin>', methods=['GET'])
def getResult(usernameLogin, passwordLogin):
    #email = request.args.get('email')
    try:
        # Retrieve data from query parameters
        driver = g.driver  # Get the driver from the Flask global context

        link = automate_login(driver, usernameLogin, passwordLogin)
        result_dict = {"link":link}
        print(result_dict)
        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.before_request
def before_request():
    if 'driver' not in g:
        g.driver = init_driver()  # Initialize the driver if it doesn't exist in the context

if __name__ == '__main__':
    app.run(host='0.0.0.0')




