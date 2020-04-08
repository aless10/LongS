import time
from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import WebDriverWait
import config


def connect():
    driver = webdriver.Chrome(config.path_to_chrome)
    driver.maximize_window()
    return driver


def login(driver):
    driver.get(config.base_url)
    login_button = driver.find_element_by_xpath("/html/body/div[1]/esselunga-welcome-header/header/div/p/a[1]")
    login_button.click()
    mail_field = driver.find_element_by_id("gw_username")
    mail_field.send_keys(config.email)
    password_field = driver.find_element_by_id("gw_password")
    password_field.send_keys(config.password)
    remember_me = driver.find_element_by_id("rememberme")
    remember_me.click()
    login_submit = driver.find_element_by_xpath("//*[@id='loginForm']/div/button")
    login_submit.click()


def wait_for_available(driver):
    available = False
    while not available:
        print(f"Trying at {datetime.datetime.now()}")
        slots = driver.find_elements_by_xpath("//input[@class='disponibile']")

        if slots:
            available = True
            print(f"{len(slots)} slots found.")
            slots[0].click()
            driver.save_screenshot(f"{datetime.datetime.now()}_slots_found.png")
            driver.find_element_by_id("checkoutNextStep").click()
        else:
            print("No slot available. Retrying in 1 minute")
            time.sleep(3600)
            driver.refresh()
            time.sleep(3)
            click_next_step(driver)


def click_next_step(driver):
    next_step_button = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("checkoutNextStep"))
    next_step_button.click()


def main():
    d = connect()
    with d as driver:
        print("Login")
        login(driver)
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
        click_next_step(driver)
        print("Completed!")


if __name__ == '__main__':
    main()
