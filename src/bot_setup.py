import logging as log
import google.cloud.logging
import os
import random
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import driver_setup as driver_setup

meme_img_list = list()
user_tags = list()

driver = driver_setup.get_chrome_driver()
scheduler = BlockingScheduler()

memespath = os.getcwd() + "/img/"
user = "mafiabot123@gmail.com"
pw = os.environ['BOTPW'].replace('\\', '')
test_id = "3724459277571389"
mafia_id = "1758853220817730"
url = "https://www.facebook.com/messages/t/" + test_id


def print_tags():
    text_area = None

    # TODO - timeout
    # timeout - need to set as property in file
    timeout = 55

    log.info("Found @Bot tag. Printing Users '@' Tags... ")

    for name in user_tags:
        text_area = driver.switch_to.active_element
        text_area.send_keys(name)
        text_area = driver.switch_to.active_element
        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)
        time.sleep(.05)
        text_area.send_keys(Keys.ARROW_UP)
        time.sleep(.05)
        text_area.send_keys(Keys.SPACE)

    time.sleep(.05)
    text_area.send_keys(Keys.ENTER)
    text_area = driver.switch_to.active_element
    time.sleep(.05)
    text_area.send_keys("Next poll available in {:d} seconds.".format(timeout + 5))
    time.sleep(.05)
    text_area.send_keys(Keys.ENTER)

    log.info("Done tagging.")

    log.info("Sleeping for {:d} seconds.".format(timeout))
    time.sleep(timeout)


def print_meme():

    log.info("Found @Bot meme tag. Sending Random Meme... ")

    img = memespath + "/" + random.choice(meme_img_list)

    img_input = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[3]/div[2]/form/div/span/input')

    time.sleep(.05)
    img_input.send_keys(img)
    time.sleep(.05)
    text_area = driver.switch_to.active_element
    time.sleep(.05)
    text_area.send_keys(Keys.ENTER)

    log.info("Meme sent.")

    driver.refresh()


def print_help():
    text_area = driver.switch_to.active_element
    time.sleep(.05)
    message = "Available commands:\n'@Matthew Botte' => Tags all of the conversation members.\n'@Matthew Botte " \
              "update' => Updates the conversation member list - use after adding/removing people.\n'@Matthew " \
              "Botte meme' => Sends a random meme. "
    text_area.send_keys(message)
    time.sleep(.05)
    text_area = driver.switch_to.active_element
    text_area.send_keys(Keys.ENTER)


def search_tagging():
    global user_tags

    src = driver.page_source
    meme_found = "@Matthew Botte</a></div><span> meme" in src
    tag_found = "@Matthew Botte</a></div></" in src
    help_found = "@Matthew Botte</a></div><span> help" in src
    update_found = "@Matthew Botte</a></div><span> update" in src

    if meme_found:
        print_meme()
        time.sleep(5)

    if tag_found:
        print_tags()
        time.sleep(5)

    if help_found:
        print_help()
        time.sleep(5)

    if update_found:
        update_conf_participants(False)
        time.sleep(5)

    if meme_found or tag_found or help_found or update_found:
        hide_bot_tags()


def hide_bot_tags():
    element_list = driver.find_elements_by_xpath("//*[contains(text(), '@Matthew Botte')]")
    js = "var element = arguments[0];element.parentNode.removeChild(element);"
    for element in element_list:
        driver.execute_script(js, element)


def update_conf_participants(initflag):
    global user_tags

    tag_names = driver.find_elements_by_class_name('_8slc')
    tag_names = [x.text for x in tag_names]
    tag_names = ["@" + name + " " for name in tag_names]
    tag_names = [name for name in tag_names if name != "@Matthew Botte "]
    tag_names = [name.split(" ")[0] for name in tag_names]

    if not initflag:
        text_area = driver.switch_to.active_element
        time.sleep(.05)
        text_area.send_keys("Updated conversation user list.")
        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)

    log.info("Updated conversation user list.")
    log.info(tag_names)
    user_tags = tag_names


@scheduler.scheduled_job('interval', seconds=10)
def main_loop():
    try:

        log.debug("Checking for request now. (interval = {:d}s)".format(10))
        search_tagging()

    except KeyboardInterrupt:
        driver.close()


@scheduler.scheduled_job('interval', hours=1)
def refresh_page():
    driver.refresh()


def main():
    logclient = google.cloud.logging.Client()
    logclient.get_default_handler()
    logclient.setup_logging()
    log.basicConfig(filename='botlogs.log', level=log.DEBUG, filemode='w')

    driver.get(url)

    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))

    username_box = driver.find_element_by_xpath('//*[@id="email"]')
    username_box.send_keys(user)
    password_box = driver.find_element_by_xpath('//*[@id="pass"]')
    password_box.send_keys(pw)
    password_box.send_keys(Keys.RETURN)

    time.sleep(2)
    update_conf_participants(True)
    hide_bot_tags()

    log.info(driver.current_url)
    log.info("Logged in, waiting for requests...")

    scheduler.start()


if __name__ == "__main__":
    meme_img_list = os.listdir(memespath)
    print(len(meme_img_list))
    main()
