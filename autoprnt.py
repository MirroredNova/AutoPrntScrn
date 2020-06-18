import datetime
import string
import random
import requests
import shutil

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


lower_alphabet = string.ascii_lowercase + "1234567890"
base_url = "https://prnt.sc/"


def get_suffix():
    with open("suffixes.txt", "a") as myfile:
        with open("suffixes.txt", "r") as readfile:
            suffix = ""
            for j in range(6):
                suffix += random.choice(lower_alphabet)

            if suffix in readfile.read():
                suffix = get_suffix()

            myfile.write(suffix + '\n')
    return suffix


def main():
    repeats = int(input("How many images would you like: "))
    begin_time = datetime.datetime.now()
    driver = webdriver.Chrome()
    for i in range(repeats):

        suffix = get_suffix()
        print(suffix)
        driver.get(base_url + suffix)

        try:
            image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img[@id='screenshot-image']")))
        except TimeoutException:
            print("The suffix " + suffix + " is invalid")
            continue

        response = requests.get(image.get_attribute('src'), stream=True)
        with open('ImageDump/' + suffix + '.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    print(datetime.datetime.now() - begin_time)
    driver.close()


main()
