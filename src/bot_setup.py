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


class BotApp:
    # TODO - dynamiczne/reczne updatowanie listy uczestników
    # TODO  - trzeba ogarnac plik config.ini - libka configparser
    # config = configparser.ConfigParser()
    # config.read('config.ini')

    driver = driver_setup.get_chrome_driver()

    memespath = os.getcwd() + "/img/"
    user = "mafiabot123@gmail.com"
    pw = os.environ['BOTPW'].replace('\\', '')
    test_id = "3724459277571389"
    mafia_id = "1758853220817730"
    url = "https://www.facebook.com/messages/t/" + mafia_id

    @staticmethod
    def print_tags():

        global user_tags
        text_area = None

        # TODO - timeout
        # timeout - need to set as property in file
        timeout = 55

        log.info("Found @Bot tag. Printing Users '@' Tags... ")

        for name in user_tags:
            text_area = BotApp.driver.switch_to.active_element
            text_area.send_keys(name)
            text_area = BotApp.driver.switch_to.active_element
            time.sleep(.05)
            text_area.send_keys(Keys.ENTER)
            time.sleep(.05)
            text_area.send_keys(Keys.ARROW_UP)
            time.sleep(.05)
            text_area.send_keys(Keys.SPACE)

        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)
        text_area = BotApp.driver.switch_to.active_element
        time.sleep(.05)
        text_area.send_keys("Next poll available in {:d} seconds.".format(timeout + 5))
        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)

        log.info("Done tagging.")

        log.info("Sleeping for {:d} seconds.".format(timeout))
        time.sleep(timeout)

    @staticmethod
    def print_meme():
        driver = BotApp.driver

        log.info("Found @Bot meme tag. Sending Random Meme... ")

        img = BotApp.memespath + "/" + random.choice(meme_img_list)

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

    @staticmethod
    def print_help():
        text_area = BotApp.driver.switch_to.active_element
        time.sleep(.05)
        message = "Available commands:\n'@Matthew Botte' => Tags all of the conversation members.\n'@Matthew Botte " \
                  "update' => Updates the conversation member list - use after adding/removing people.\n'@Matthew " \
                  "Botte meme' => Sends a random meme. "
        text_area.send_keys(message)
        time.sleep(.05)
        text_area = BotApp.driver.switch_to.active_element
        text_area.send_keys(Keys.ENTER)

    @staticmethod
    def search_tagging():

        global user_tags

        src = BotApp.driver.page_source
        meme_found = "@Matthew Botte</a></div><span> meme" in src
        tag_found = "@Matthew Botte</a></div></" in src
        help_found = "@Matthew Botte</a></div><span> help" in src
        update_found = "@Matthew Botte</a></div><span> update" in src

        if meme_found:
            BotApp.print_meme()
            time.sleep(5)
            BotApp.hide_bot_tags()

        if tag_found:
            BotApp.print_tags()
            time.sleep(5)
            BotApp.hide_bot_tags()

        if help_found:
            BotApp.print_help()
            time.sleep(5)
            BotApp.hide_bot_tags()

        if update_found:
            BotApp.update_conf_participants(False)
            time.sleep(5)
            BotApp.hide_bot_tags()

    @staticmethod
    def hide_bot_tags():
        element_list = BotApp.driver.find_elements_by_xpath("//*[contains(text(), '@Matthew Botte')]")
        js = "var element = arguments[0];element.parentNode.removeChild(element);"
        for element in element_list:
            BotApp.driver.execute_script(js, element)

    @staticmethod
    def update_conf_participants(initflag):

        global user_tags

        tag_names = BotApp.driver.find_elements_by_class_name('_8slc')
        tag_names = [x.text for x in tag_names]
        tag_names = ["@" + name + " " for name in tag_names]
        tag_names = [name for name in tag_names if name != "@Matthew Botte "]
        tag_names = [name.split(" ")[0] for name in tag_names]

        if not initflag:
            text_area = BotApp.driver.switch_to.active_element
            time.sleep(.05)
            text_area.send_keys("Updated conversation user list.")
            time.sleep(.05)
            text_area.send_keys(Keys.ENTER)

        log.info("Updated conversation user list.")
        log.info(tag_names)
        user_tags = tag_names

    @staticmethod
    @scheduler.scheduled_job('interval', seconds=10)
    def main_loop():

        try:

            log.debug("Checking for request now. (interval = {:d}s)".format(10))
            BotApp.search_tagging()

        except KeyboardInterrupt:
            BotApp.driver.close()

    @staticmethod
    @scheduler.scheduled_job('interval', hours=1)
    def refresh_page():
        BotApp.driver.refresh()

    @staticmethod
    def main():

        global user_tags

        lclient = google.cloud.logging.Client()
        lclient.get_default_handler()
        lclient.setup_logging()
        log.basicConfig(filename='botlogs.log', level=log.DEBUG, filemode='w')

        driver = BotApp.driver

        driver.get(BotApp.url)

        WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))

        username_box = driver.find_element_by_xpath('//*[@id="email"]')
        username_box.send_keys(BotApp.user)
        password_box = driver.find_element_by_xpath('//*[@id="pass"]')
        password_box.send_keys(BotApp.pw)
        password_box.send_keys(Keys.RETURN)

        time.sleep(2)
        BotApp.update_conf_participants(True)
        BotApp.hide_bot_tags()

        log.info(driver.current_url)
        log.info("Logged in, waiting for requests...")

        scheduler = BlockingScheduler()
        scheduler.start()


if __name__ == "__main__":
    meme_img_list = os.listdir(BotApp.memespath)
    print(len(meme_img_list))
    BotApp.main()
