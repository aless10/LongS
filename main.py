import os
import sys
import time

import datetime
import logging
import click as click
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from send_mail import send_mail

WEB_DRIVER = os.environ.get("WEB_DRIVER")
BASE_URL = "https://www.esselungaacasa.it/ecommerce/nav/welcome/index.html"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
HTML_PATH = os.path.join(os.path.dirname(__file__), "html")

RETRY_TIME = 60
MAX_TENTATIVE = 30


log = logging.getLogger("esselunga")
log_filename = os.environ.get("LOG_FILEPATH", os.path.join(os.path.dirname(__file__), 'esselunga.log'))
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_filename,
                    filemode='a')
log.info("Logger initialized correctly. The log file is at %s", log_filename)


def connect():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def save_html(driver, filename):
    with open(os.path.join(HTML_PATH, f"{filename}.html"), "w") as writer:
        writer.write(driver.page_source)


def is_basket_full(driver):
    time.sleep(5)
    basket_items = driver.find_elements_by_xpath("//*[@id='shoppingTabList']/ul/li/a/span/span")[0].text
    if int(basket_items) == 0:
        log.info("No Items in the basket. Leaving...")
        sys.exit(0)


def login(driver):
    driver.get(BASE_URL)
    save_html(driver, "login")
    time.sleep(5)
    login_button = driver.find_element_by_xpath("/html/body/div[1]/esselunga-welcome-header/header/div/p/a[1]")
    login_button.click()
    time.sleep(5)
    mail_field = driver.find_element_by_id("gw_username")
    mail_field.send_keys(EMAIL)
    password_field = driver.find_element_by_id("gw_password")
    password_field.send_keys(PASSWORD)
    remember_me = driver.find_element_by_id("rememberme")
    remember_me.click()
    login_submit = driver.find_element_by_xpath("//*[@id='loginForm']/div/button")
    login_submit.click()


def wait_for_available(driver):
    save_html(driver, "slots")
    tentative = 0

    while tentative < MAX_TENTATIVE:
        log.info(f"Trying at {datetime.datetime.now()}")
        slots = driver.find_elements_by_xpath("//input[@class='disponibile']")

        if slots:
            log.info(f"{len(slots)} slots found.")
            send_mail(EMAIL,
                      subject="[BOT] Free slots found!",
                      body=f"{datetime.datetime.now()}: {len(slots)} slots found!\nWe select the first available.")
            slots[0].click()
            driver.save_screenshot(f"{datetime.datetime.now()}_slots_found.png")
            driver.find_element_by_id("checkoutNextStep").click()
            return
        else:
            tentative += 1
            log.info(f"No slots available. Retrying in {RETRY_TIME} seconds")
            time.sleep(RETRY_TIME)
            driver.refresh()
            time.sleep(3)
            click_next_step(driver)

    sys.exit(0)


def click_next_step(driver):
    next_step_button = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("checkoutNextStep"))
    next_step_button.click()


@click.command()
def main():
    tentative = 0
    logged = False
    while not logged and tentative < MAX_TENTATIVE:
        tentative += 1
        log.info(f"Tentative #{tentative}")
        try:
            d = connect()
            logged = True
            with d as driver:
                start = datetime.datetime.now()
                log.info("Login")
                login(driver)
                # Check if the basket is full or not. If no items => exit
                is_basket_full(driver)
                # Go checkout!
                time.sleep(2)
                go_checkout = driver.find_element_by_id("cassa")
                go_checkout.click()
                time.sleep(2)
                log.info("Basket")
                click_next_step(driver)
                time.sleep(2)
                wait_for_available(driver)
                log.info("Pay!")
                time.sleep(5)
                save_html(driver, "pay")
                click_next_step(driver)
                log.info("Confirm!")
                time.sleep(5)
                save_html(driver, "confirm_checkout")
                click_next_step(driver)
                log.info("Completed!")
                save_html(driver, "completed")
                end = datetime.datetime.now()
                log.info(f"It took {end - start}")
                log.info("Sending confirmation email")
                send_mail(EMAIL)
        except Exception as e:
            log.info(f"An exception occurred: {e}")
            logged = False


if __name__ == "__main__":
    main()
