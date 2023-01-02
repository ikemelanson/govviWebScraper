import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
import pyperclip
import time

ranks = {
    '1': '//*[@id="kt_wrapper"]/div[2]/div[2]/div[2]/div[1]/a/div/div',
    '2': '//*[@id="kt_wrapper"]/div[2]/div[2]/div[2]/div[2]/a/div/div',
    '3': '//*[@id="kt_wrapper"]/div[2]/div[2]/div[2]/div[3]/a/div/div',
    '4': '//*[@id="kt_wrapper"]/div[2]/div[2]/div[2]/div[4]/a/div/div',
    '5': '//*[@id="kt_wrapper"]/div[2]/div[2]/div[2]/div[5]/a/div/div'
}

# input date to grab
dateToGrab = input("Date to grab: ")
dateToGrab = datetime.strptime(dateToGrab, "%Y-%m-%d")
chooseRank = input("Rank 1-5: ")
username = input("Username: ")
password = input("Password: ")

caps = DesiredCapabilities().SAFARI
caps["pageLoadStrategy"] = "none"

driver = webdriver.Safari(desired_capabilities=caps, executable_path = '/Library/Apple/System/Library/CoreServices/SafariSupport.bundle/Contents/MacOS/safaridriver')
driver.set_window_size(1440, 820)
driver.get("https://www.govvi.com/adminlogin")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="kt_body"]/div/div/div/div/form/div[2]/input'))).send_keys(username)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="kt_body"]/div/div/div/div/form/div[3]/input'))).send_keys(password)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'kt_sign_in_submit'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="#kt_aside_menu"]/div[2]/a'))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ranks[chooseRank]))).click()
time.sleep(5)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

done = False
pageNo = 1
found = False
final = ''

while done == False or found == False:
    pageLinks = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ranktable_wrapper"]/div[2]')))
    table = driver.find_element(By.XPATH, '//*[@id="ranktable"]/tbody')
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        cell = row.find_elements(By.TAG_NAME, 'td')
        if datetime.strptime(cell[7].text, "%Y-%m-%d") == dateToGrab:
            found = True
            final += cell[2].text + cell[3].text + '\n'

        elif datetime.strptime(cell[7].text, "%Y-%m-%d") != dateToGrab and found == True:
            done = True
            break
    
    if done == False:
        pageNo +=1
        pageLinks.find_element(By.LINK_TEXT, str(pageNo)).click()

pyperclip.copy(final)
print(final)