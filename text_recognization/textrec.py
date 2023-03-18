import pytesseract
import cv2
import numpy as np
import re

def runner(filepath):
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kevin\AppData\Local\Tesseract-OCR\tesseract.exe'

    def finishing(img):
        kernal = np.ones((5,5), np.uint8)
        img = cv2.erode(img, kernal, iterations = 1)
        img = cv2.dilate(img, kernal, iterations = 1)
        return img

    img = cv2.imread(filepath)
    edit = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edit = cv2.threshold(edit, 127, 255, cv2.THRESH_OTSU)[1]
    edit = cv2.medianBlur(edit, 3)
    # edit = finishing(edit) #costco best without

    text = pytesseract.image_to_string(cv2.cvtColor(edit, cv2.COLOR_BGR2RGB), config='--psm 4 --oem 3')

    pattern = r'([0-9]+\.[0-9])'
    ret = []
    for row in text.split('\n'):
        if (re.search(pattern, row) is not None 
            and re.search('AMOUNT', row) is None
            and re.search('TAX', row) is None
            and re.search('SUBTOTAL', row) is None):
            ret.append(row)

    prices= {}
    pattern2 = r'([0-9]+\.[0-9]+-A)'
    past = ""
    
    for row in ret:
        curr = ""
        words = row.split()
        for i, word in enumerate(words):
            if re.search(pattern2, word):
                temp = word[:len(word) - 2] # gets only the discounted price
                prices[past] = round(prices[past] - float(temp), 2)
                break

            if re.search(pattern, word):
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

#     #testing purposes only
#     for item in prices:
#         print(item + ": " + str(prices[item]))

def main():
    print(runner('test_images/costco7.jpg'))

if __name__ == "__main__":
    main()