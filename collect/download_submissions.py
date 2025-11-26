from time import sleep

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Use webdriver-manager (recommended)
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

driver.implicitly_wait(5)

driver.get("https://electricsheep.teachable.com/admin-app/courses/2778348/reports/open-ended-questions")

if driver.find_element(By.ID, "login-with-password-link"):
    driver.find_element(By.ID, "login-with-password-link").click()

    sleep(1) # Wait for the login form to load

    driver.find_element(By.ID, "email").send_keys("asheemsingh@gmail.com")
    driver.find_element(By.ID, "password").send_keys("liv543v3r")

    sleep(1) # Wait for CAPTCHA

    driver.find_element(By.XPATH, "/html/body/main/div/form/div[4]/input").click()

    sleep(5) # Wait for the login to complete

button = driver.find_element(By.XPATH, '//button[text()="Export CSV"]')
button.click()

sleep(20)

driver.quit()