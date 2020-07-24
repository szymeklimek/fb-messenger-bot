import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver


def get_chrome_driver():
    os.chdir("..")

    driver_path = "/usr/lib/chromium-browser/chromedriver"

    options = ChromeOptions()

    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36")
    options.add_argument("--headless")

    driver = webdriver.Chrome(driver_path, options=options)

    return driver


def get_firefox_driver():
    os.chdir("..")

    driver_path = "/usr/local/bin"

    options = FirefoxOptions()

    options.headless = True

    driver = webdriver.Firefox(driver_path, options=options)

    return driver
