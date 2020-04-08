import os
import sys
import time

import click as click
from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import WebDriverWait

from send_mail import send_mail

CHROME_WEBDRIVER = os.path.join(os.path.dirname(__file__), "selenium/webdriver", "chrome/chromedriver")
BASE_URL = "https://www.esselungaacasa.it/ecommerce/nav/welcome/index.html"
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
HTML_PATH = os.path.join(os.path.dirname(__file__), "html")

RETRY_TIME = 60
MAX_TENTATIVE = 30


def connect():
    driver = webdriver.Chrome(CHROME_WEBDRIVER)
    driver.maximize_window()
    return driver


def save_html(driver, filename):
    with open(os.path.join(HTML_PATH, f"{filename}.html"), "w") as writer:
        writer.write(driver.page_source)


def is_basket_full(driver):
    time.sleep(2)
    basket_items = driver.find_elements_by_xpath("//*[@id='shoppingTabList']/ul/li/a/span/span")[0].text
    if int(basket_items) == 0:
        print("No Items in the basket. Leaving...")
        sys.exit(0)


def login(driver):
    driver.get(BASE_URL)
    save_html(driver, "login")
    login_button = driver.find_element_by_xpath("/html/body/div[1]/esselunga-welcome-header/header/div/p/a[1]")
    login_button.click()
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
    available = False
    while not available:
        print(f"Trying at {datetime.datetime.now()}")
        slots = driver.find_elements_by_xpath("//input[@class='disponibile']")

        if slots:
            available = True
            print(f"{len(slots)} slots found.")
            send_mail(EMAIL,
                      subject="[BOT] Free slots found!",
                      body=f"{datetime.datetime.now()}: {len(slots)} slots found!\nWe select the first available.")
            slots[0].click()
            driver.save_screenshot(f"{datetime.datetime.now()}_slots_found.png")
            driver.find_element_by_id("checkoutNextStep").click()
        else:
            print(f"No slots available. Retrying in {RETRY_TIME} seconds")
            time.sleep(RETRY_TIME)
            driver.refresh()
            time.sleep(3)
            click_next_step(driver)


def click_next_step(driver):
    next_step_button = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("checkoutNextStep"))
    next_step_button.click()


@click.command()
def main():
    tentative = 0
    logged = False
    while not logged and tentative < MAX_TENTATIVE:
        tentative += 1
        print(f"Tentative #{tentative}")
        try:
            d = connect()
            logged = True
            with d as driver:
                start = datetime.datetime.now()
                print("Login")
                login(driver)
                # Check if the basket is full or not. If no items => exit
                is_basket_full(driver)
                # Go checkout!
                time.sleep(2)
                go_checkout = driver.find_element_by_id("cassa")
                go_checkout.click()
                time.sleep(2)
                print("Basket")
                click_next_step(driver)
                time.sleep(2)
                wait_for_available(driver)
                print("Pay!")
                time.sleep(5)
                save_html(driver, "pay")
                click_next_step(driver)
                print("Confirm!")
                time.sleep(5)
                save_html(driver, "confirm_checkout")
                click_next_step(driver)
                print("Completed!")
                save_html(driver, "completed")
                end = datetime.datetime.now()
                print(f"It took {end - start}")
                print("Sending confirmation email")
                send_mail(EMAIL)
        except Exception as e:
            print(f"An exception occurred: {e}")
            logged = False


if __name__ == "__main__":
    main()
