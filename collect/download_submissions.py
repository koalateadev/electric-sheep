from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("-profile")
options.add_argument("/Users/maxbuster/Library/Caches/Firefox/Profiles/vcqgmt3w.default-release")

driver = webdriver.Firefox(options=options)

url = "https://electricsheep.teachable.com/admin-app/courses/2778348/reports/open-ended-questions"
driver.get(url)
time.sleep(5)  # Optional wait to ensure page loads

button = driver.find_element(By.LINK_TEXT, "Export CSV")
button.click()

driver.quit()