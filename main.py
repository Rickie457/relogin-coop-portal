from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
from dotenv import load_dotenv
import time
import os

load_dotenv()
# Your COOP Username
USERNAME = os.getenv("LASSONDE_USER")
# COOP Password
PASSWORD = os.environ.get("LASSONDE_PW")
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH)
driver.get("https://orbis.lassonde.yorku.ca/student/login.htm")

check = False
try:
    # Wait until the username input has loaded
    username_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "j_username")))
    username_input.send_keys(USERNAME)

    # Wait 2 more seconds to enter the password (the website can be slow)
    driver.implicitly_wait(2)
    password_input = driver.find_element(by=By.NAME, value="j_password")
    password_input.send_keys(PASSWORD)
    # Enter the password, and click return to head to the coop page.
    password_input.send_keys(Keys.RETURN)

    # wait 2 seconds for the page to load
    driver.implicitly_wait(2)
    # wait 10 seconds (max) for the navbar to load
    navBtn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/header/div[4]/div/div/button')))
    # open the navbar to reveal the nav buttons
    navBtn.click()

    # wait 5 seconds for the nav buttons to load (max)
    driver.implicitly_wait(2)
    # find the jobs button and click on it
    jobs = driver.find_element(by=By.XPATH, value='/html/body/div[2]/header/div[3]/div[1]/nav/ul/li[3]/a')
    jobs.click()
    
    driver.implicitly_wait(2)
    # find the postings button for summer 2023 and click on it 
    # THIS IS FOR SUMMER 2023 JOB POSTINGS. MAY BE CHANGED USING THE FULL XPATH.
    postings = driver.find_element(by=By.XPATH, value='/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[2]/div/div/div/div/table[1]/tbody/tr[1]/td[2]/a')
    postings.click()

    driver.implicitly_wait(5)
    # wait 5 seconds to detect the deadlines button
    deadlines = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/div/div/div/div[2]/div[3]/table/thead/tr/th[7]/a")))

    # Stops the browser from closing on its own, must be closed manually.
    while not check:
        try:
            if(driver.title):
                # you start to get signed out after 1739 seconds (28.983 minutes), so wait 5 seconds then search for the button.
                wait = WebDriverWait(driver, 1744)
                # wait for the button to be clickable (e.g. display--none is removed and opacity=1 from the websites functions) and click on it.
                loginBtn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/button[2]')))
                print("FOUND PROMPT")
                loginBtn.click()
                print("LOGGED BACK IN!")
        except:
            # Manually closed the session.
            print("USER HAS CLOSED THE SESSION.")
            # Stop the loop, continue to finally.
            check = True

# If anything else goes wrong, quit and dispose everything.
except:
    driver.quit()

# Quit and dispose everything.
finally:
    driver.quit()