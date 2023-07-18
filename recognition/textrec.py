import pytesseract
import cv2 as cv
import numpy as np
import re
import imutils
import corners
import preprocess
from skimage.filters import threshold_local


def costco_pattern(text):
    pattern1 = r'([0-9]+\.[0-9])'
    pattern2 = r'([0-9]+\:[0-9])' # account for blue strips in costco reciepts
    ret = []
    for row in text.split('\n'):
        if ((re.search(pattern1, row) or re.search(pattern2, row))
            and re.search('AMOUNT', row) is None
            and re.search('TAX', row) is None
            and re.search('SUBTOTAL', row) is None):
            ret.append(row)

    prices= {}
    pattern3 = r'([0-9]+\.[0-9]+-A)'
    past = ""
    
    for row in ret:
        curr = ""
        words = row.split()
        for i, word in enumerate(words):
            if re.search(pattern3, word):
                temp = word[:len(word) - 2] # gets only the discounted price
                prices[past] = round(prices[past] - float(temp), 2)
                break

            if re.search(pattern1, word) or re.search(pattern2, word):
                word = word.replace(':', '.')
                if len(curr) > 0:
                    if curr in prices:
                        prices[curr] = round(prices[curr] + float(word), 2)
                    else: 
                        prices[curr] = float(word)
                break # do not want anything after price

            if i == 0 and word == 'E':
                continue
                # for costco receipts do not want the E tag

            if word.isnumeric():
                continue
                # do not want random numbers

            # add all other item descriptors
            curr += word + " "
        past = curr
    return prices



def process_text(img):
    text = pytesseract.image_to_string(cv.cvtColor(img, cv.COLOR_BGR2RGB), config='--psm 4 --oem 3')
    formatted = costco_pattern(text)
    print(formatted)

    
def testing(path):
    warped = preprocess.perspectiveTransform(path)
    filtered = preprocess.filter_img(warped)
    process_text(filtered)


if __name__ == "__main__":
    testing("recognition/test_images/costco.jpg")
