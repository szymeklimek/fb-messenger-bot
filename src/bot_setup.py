import logging as log
import google.cloud.logging
import os
import random
import time
import psutil

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import driver_setup as driver_setup

meme_img_list = list()


class BotApp:

    # TODO - dynamiczne/reczne updatowanie listy uczestników
    # TODO  - trzeba ogarnac plik config.ini - libka configparser
    # config = configparser.ConfigParser()
    # config.read('config.ini')

    memespath = "/home/szklimowicz/fb-messenger-bot/img/"
    user = "mafiabot123@gmail.com"
    pw = os.environ['BOTPW'].replace('\\', '')
    test_id = "3724459277571389"
    mafia_id = "1758853220817730"
    url = "https://www.facebook.com/messages/t/" + mafia_id

    driver = driver_setup.get_chrome_driver()

    @staticmethod
    def print_tags(driver, tags):

        text_area = None

        log.info("Bot has been tagged: Printing Users '@' Tags... ")

        for name in tags:
            text_area = driver.switch_to.active_element
            text_area.send_keys(name)
            text_area = driver.switch_to.active_element
            time.sleep(.05)
            text_area.send_keys(Keys.ENTER)
            time.sleep(.05)
            text_area.send_keys(Keys.ARROW_UP)
            time.sleep(.05)
            text_area.send_keys(Keys.SPACE)

        timeout = 60

        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)
        text_area = driver.switch_to.active_element
        time.sleep(.05)
        text_area.send_keys("Next poll available in {:d} seconds.".format(timeout))
        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)

        log.info("Done tagging.")

        # TODO - timeout
        # timeout - need to set as property in file

        log.info("Sleeping for {:d} seconds.".format(timeout))
        time.sleep(timeout)

    @staticmethod
    def print_meme(driver):

        log.info("Bot has been tagged: Sending Random Meme... ")

        img_path = BotApp.memespath + "/" + random.choice(meme_img_list)

        # try:
        #     img_input = driver.find_element_by_xpath(
        #         '/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[3]/div[2]/form/div/span/input')
        # except:
        #     img_input = driver.find_element_by_xpath(
        #         '/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[3]/div[2]/form/div/span/div/input')
        #     pass

        img_input = driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div/div/div[2]/span/div[2]/div[2]/div[2]/div/div[3]/div[2]/form/div/span/input')

        time.sleep(.05)
        img_input.send_keys(img_path)
        time.sleep(.05)
        text_area = driver.switch_to.active_element
        time.sleep(.05)
        text_area.send_keys(Keys.ENTER)

        log.info("Meme sent.")

    @staticmethod
    def search_tagging(driver, tags):

        src = driver.page_source
        meme_found = "@Matthew Botte</a></div><span> meme" in src  # re.search('@Matthew Botte -meme', src)
        tag_found = "@Matthew Botte</a></div></" in src  # re.search('@Matthew Botte', src)

        if meme_found:

            log.info("Found @Bot meme tag.")
            BotApp.print_meme(driver)
            # needs to pause for a while after sending, else breaks
            # time.sleep(10)
            time.sleep(5)
            driver.get(BotApp.url)
            time.sleep(5)
            BotApp.hide_bot_tags(driver)

        # else:
        #     log.info("Did not find @Bot meme tag.")

        if tag_found:

            log.info("Found @Bot tag.")
            BotApp.print_tags(driver, tags)
            BotApp.hide_bot_tags(driver)

        # else:
        #     log.info("Did not find @Bot tag.")

    @staticmethod
    def hide_bot_tags(driver):
        element_list = driver.find_elements_by_xpath("//*[contains(text(), '@Matthew Botte')]")
        for element in element_list:
            driver.execute_script("var element = arguments[0];element.parentNode.removeChild(element);", element)

    @staticmethod
    def main_loop(driver, tags):

        while True:
            try:

                # probably not needed - driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                log.info("Checking for request in 5...")
                time.sleep(5)
                log.info("Checking now.")
                BotApp.search_tagging(driver, tags)

            except KeyboardInterrupt:
                driver.close()

    @staticmethod
    def main():
        
        lclient = google.cloud.logging.Client()
        lclient.get_default_handler()
        lclient.setup_logging()
        log.basicConfig(filename='botlogs.log', level=log.DEBUG, filemode='w')

        driver = BotApp.driver

        BotApp.driver.get(BotApp.url)

        WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))

        username_box = driver.find_element_by_xpath('//*[@id="email"]')
        username_box.send_keys(BotApp.user)
        password_box = driver.find_element_by_xpath('//*[@id="pass"]')
        password_box.send_keys(BotApp.pw)
        password_box.send_keys(Keys.RETURN)

        log.info(driver.current_url)

        #time.sleep(10)

        tag_names = driver.find_elements_by_class_name('_8slc')
        tag_names = [x.text for x in tag_names]
        tag_names = ["@" + name + " " for name in tag_names]
        tag_names = [name for name in tag_names if name != "@Matthew Botte "]
        tag_names = [name.split(" ")[0] for name in tag_names]

        #p = psutil.Process(driver.service.process.pid)

        log.info(tag_names)
        log.info("Logged in, waiting for requests...")
        # log.info(p.__getattribute__("pid"))
        # for process in p.children(recursive=True):
        #     log.info(process.__getattribute__("pid"))

        BotApp.hide_bot_tags(driver)

        #time.sleep(10)

        BotApp.main_loop(driver, tag_names)


if __name__ == "__main__":
    meme_img_list = os.listdir(BotApp.memespath)

    BotApp.main()
