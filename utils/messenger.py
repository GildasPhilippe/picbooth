import os
import time

from dotenv import load_dotenv, find_dotenv

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv(find_dotenv())


def open_messenger() -> WebDriver:
    driver = webdriver.Firefox()

    conversation_id = os.getenv("FB_CONVERSATION_ID")
    conversation_url = f"https://www.facebook.com/messages/t/{conversation_id}"

    driver.get(conversation_url)

    if "Connexion ou inscription" in driver.title or "Se connecter" in driver.title:
        email, password = os.getenv("FB_EMAIL"), os.getenv("FB_PASSWORD")

        elem = driver.find_element(By.ID, "email")
        elem.send_keys(email)
        elem = driver.find_element(By.ID, "pass")
        elem.send_keys(password)
        elem.submit()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type=file]")))

    return driver


def send_picture(picture: str, driver: WebDriver):

    nb_icons_start = get_nb_icons(driver)

    upload_file = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
    print("upload file = ", upload_file)
    upload_file.send_keys(picture)
    print("picture sent")

    ct = 0
    while get_nb_icons(driver) <= nb_icons_start and ct < 5:
        print("ct = ", ct)
        print(get_nb_icons(driver), " VS ", nb_icons_start)
        time.sleep(1)
        ct += 1

    print("sending enter")
    print(get_nb_icons(driver), " VS ", nb_icons_start)
    # upload_file.submit()

    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()


def get_nb_icons(driver):
    return len(driver.find_elements(By.CSS_SELECTOR, "div[role=button] > i"))


if __name__ == "__main__":
    firefox = open_messenger()
    send_picture(os.path.abspath("../pictures/test.jpg"), firefox)
    input("Close ?")
    firefox.close()
