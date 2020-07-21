from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import re
import os

os.chdir("..")

driver_path = os.getcwd() + "\driver\chromedriver.exe"

ff_options = Options()

prefs = {"profile.default_content_setting_values.notifications" : 2}

ff_options.add_experimental_option("prefs",prefs)
ff_options.add_argument("--disable-extensions")
ff_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
ff_options.add_argument("--headless")
# chrome_options.headless = True # also works


USEREMAIL = "mafiabot@gmail.com"
USERPASSWORD = "*jK`=s:5kV]}Ub>*"
USERTARGET = "1758853220817730"

userTargetUrl = "https://www.facebook.com/messages/t/" + USERTARGET

driver = webdriver.Chrome(driver_path, options=ff_options)
driver.get(userTargetUrl)

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))

#username_box = driver.find_element_by_id('email')

username_box = driver.find_element_by_xpath('//*[@id="email"]')
username_box.send_keys(USEREMAIL)
password_box = driver.find_element_by_xpath('//*[@id="pass"]')
password_box.send_keys(USERPASSWORD)
password_box.send_keys(Keys.RETURN)

print(driver.current_url)

bot_alias = ["@Matthew Botte", "@Matthew", "Botte"]

tag_names = driver.find_elements_by_class_name('_8slc')
tag_names = [x.text for x in tag_names]
tag_names = ["@" + name + " " for name in tag_names]
tag_names = [name for name in tag_names if name != "@Matthew Botte "]
tag_names = [name.split(" ")[0] for name in tag_names]
print(tag_names)

def print_tags(tags):

    for name in tags:
        text_area = driver.switch_to.active_element
        text_area.send_keys(name)
        text_area = driver.switch_to.active_element
        time.sleep(.1)
        print("pushing enter")
        text_area.send_keys(Keys.ENTER)
        time.sleep(.1)
        print("pushing arrow")
        text_area.send_keys(Keys.ARROW_UP)
        time.sleep(.1)
        print("pushing space")
        text_area.send_keys(Keys.SPACE)

    time.sleep(.1)
    print("pushing all")
    text_area.send_keys(Keys.ENTER)
    text_area = driver.switch_to.active_element
    time.sleep(.1)
    text_area.send_keys("Next poll available in 1 minute.")
    time.sleep(.1)
    text_area.send_keys(Keys.ENTER)
    time.sleep(60)

def do_stuff(tags):
    driver.get(userTargetUrl)
    src = driver.page_source
    text_found = re.search('@Matthew Botte', src)
    if(text_found != None):
        print_tags(tags)
        print("okej")
    else:
        print("nieokej")

print("Ready")
while(True):
    try:
        print("Checking for request in 10...")
        time.sleep(10)
        print("Checking...")
        do_stuff(tag_names)
    except KeyboardInterrupt:
        driver.close()

# while(True):
#     print("waiting 5 secs")
#     time.sleep(5)
#     bot_tags = driver.find_elements_by_class_name("_ih- _p")
#     print(bot_tags)
#     for tag in bot_tags:
#         if(tag.text in bot_alias):
#             print("success")
