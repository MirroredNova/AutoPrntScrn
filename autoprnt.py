import datetime
import shutil
import string
import random
import requests
import timeit
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

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
    for i in range(repeats):
        suffix = get_suffix()
        print(suffix)

        try:
            response1 = requests.get(base_url + suffix, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response1.content.decode("utf-8"), features="html.parser")
            imgsrc = soup.find('img', attrs={'id': 'screenshot-image'})['src']
        except Exception:
            continue

        validate = URLValidator()
        try:
            validate(imgsrc)
        except ValidationError:
            imgsrc = "https:" + imgsrc

        response2 = requests.get(imgsrc, stream=True)
        with open('ImageDump/' + suffix + '.png', 'wb') as out_file:
            shutil.copyfileobj(response2.raw, out_file)
        del response2

    print(datetime.datetime.now() - begin_time)

main()
