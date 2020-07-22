import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def get_driver():

    os.chdir("..")

    driver_path = os.getcwd() + "\driver\chromedriver.exe"

    chrome_options = Options()

    prefs = {"profile.default_content_setting_values.notifications": 2}

    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(driver_path, options=chrome_options)

    driver.maximize_window()

    return driver
