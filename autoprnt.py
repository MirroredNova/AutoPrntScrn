import datetime
import os
import shutil
import string
import random

import imagehash
import requests
from PIL import Image
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

lower_alphabet = string.ascii_lowercase + "1234567890"  # set of suffix options
base_url = "https://prnt.sc/"  # base url


def get_suffix():
    """
    Opens suffix file, creates new suffix and append to list so its never used again.
    :return: str suffix
    """
    with open("suffixes.txt", "a") as myfile:  # open existing file
        with open("suffixes.txt", "r") as readfile:
            suffix = ""
            for j in range(6):  # get six characteres
                suffix += random.choice(lower_alphabet)

            if suffix in readfile.read():  # if it exists, do again
                suffix = get_suffix()

            myfile.write(suffix + '\n')  # add to file
    return suffix


def main():
    """
    Main run script
    :return: None
    """
    repeats = int(input("How many images would you like: "))  # ask for number of images to get
    begin_time = datetime.datetime.now()  # start time
    for i in range(repeats):
        suffix = get_suffix()  # get suffix
        print(suffix)

        try:  # attempt to get that suffix
            response1 = requests.get(base_url + suffix, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response1.content.decode("utf-8"), features="html.parser")
            imgsrc = soup.find('img', attrs={'id': 'screenshot-image'})['src']  # finds image in HTML
        except Exception:  # if it doesn't exist, skip and get new suffix
            continue

        validate = URLValidator()
        try:  # try to retrieve image source
            validate(imgsrc)
        except ValidationError:
            imgsrc = "https:" + imgsrc

        response2 = requests.get(imgsrc, stream=True)  # get the image source
        with open('ImageDump/' + suffix + '.png', 'wb') as out_file:  # dump image to folder
            shutil.copyfileobj(response2.raw, out_file)
        del response2

        # check if image is equal to the defaulturl image
        hash1 = imagehash.average_hash(Image.open("ImageDump/BaseImage.png"))
        hash2 = imagehash.average_hash(Image.open("ImageDump/" + suffix + ".png"))

        if hash1 - hash2 < 5:  # remove if bad image
            os.remove("ImageDump/" + suffix + ".png")
            print("Image " + suffix + " removed.")

    print("Total runtime: " + str(datetime.datetime.now() - begin_time))  # print time


main()
