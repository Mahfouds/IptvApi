from flask import Flask, jsonify, g,request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["DEBUG"]=True
CORS(app)


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'chdaouiimahfoudd@gmail.com'
app.config['MAIL_PASSWORD'] = '123456'
mail = Mail(app)


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
def automate_login(driver, usernameLogin, passwordLogin,plan):
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

    #by_text=select_option_by_text(driver,"package","Paid Trial")
    # if "-" in plan:
    #     # Replace the hyphen with a space
    #     plan = plan.replace("-", " ")
    by_text=select_option_by_text(driver,"package",plan)
    print(plan)
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
       
    


@app.route('/getResult/', methods=['POST'])
def getResult():
    try:
        # Retrieve data from form data
        usernamePost = request.form.get('username')
        passwordPost = request.form.get('password')

        # Retrieve data from query parameters
        #driver = g.driver  # Get the driver from the Flask global context

        # Perform your desired actions with usernamePost and passwordPost
        print(usernamePost, passwordPost)

        # Clean up and exit the driver
        # cleanup_driver(driver)

        # Return a response if needed
        return "Data received successfully"
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get recipient email address from the form
        recipient_email = request.form['recipient_email']

        # Create a Message object
        message = Message('Subject of the email', recipients=[recipient_email])

        # Add the body of the email
        message.body = 'Hello, this is the body of the email.'

        # Send the email
        mail.send(message)

        flash('Email sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending email: {str(e)}', 'error')

    return "except"
    
# Define a Flask route for automation using GET method
@app.route('/getResult/<string:usernameLogin>/<string:passwordLogin>/<string:usernameClient>/<string:passwordClient>', methods=['POST'])
def renew(usernameLogin, passwordLogin,usernameClient,passwordClient):
    try:
        driver.get("http://ky-iptv.com/HckqYJZU/lines?order=0&dir=desc")
        # Input text into the "user_search" input field and press Enter
        user_search_input = driver.find_element_by_id("user_search")
        user_search_input.send_keys(usernameClient)  # Replace "Your Text Here" with the desired text
        user_search_input.send_keys(Keys.RETURN)
        # Retrieve data from request payload (JSON)
        data = request.get_json()
        plan = data.get('plan')  # Assuming 'text' is the key in your payload
        # Retrieve data from query parameters
        driver = g.driver  # Get the driver from the Flask global context
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


        link = automate_login(driver, usernameLogin, passwordLogin,plan)
        result_dict = {"link": link}

        # Clean up and exit the driver
        cleanup_driver(driver)

        return jsonify(result_dict)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.before_request
def before_request():
    if 'driver' not in g:
        g.driver = init_driver()  # Initialize the driver if it doesn't exist in the context

# Function to clean up and exit the driver
def cleanup_driver(driver):
    try:
        driver.quit()  # Assuming driver is an instance of a Selenium WebDriver
    except Exception as e:
        print(f"Error while cleaning up the driver: {e}")

if __name__ == '__main__':
    #app.run(#host='0.0.0.0')
    app.run()




