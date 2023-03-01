import pytesseract
import cv2
import numpy as np
import re

def runner():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kevin\AppData\Local\Tesseract-OCR\tesseract.exe'

    def finishing(img):
        kernal = np.ones((5,5), np.uint8)
        img = cv2.erode(img, kernal, iterations = 1)
        img = cv2.dilate(img, kernal, iterations = 1)
        return img

    img = cv2.imread("test_images/costco7.jpg")
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

    # partial = ""
    # for row in text.split():
    #     #for any white space
    #     if (re.search('AMOUNT', row) is not None
    #         or re.search('TAX', row) is not None
    #         or re.search('SUBTOTAL', row) is not None):
    #         continue

    #     if row.isalpha() and len(row) > 2:
    #         partial = partial + " " + row
    #         continue
    #     if re.search(pattern, row):
    #         partial = partial + " " + row
    #         ret.append(partial)
    #         partial = ""

    return ret

# def main():
#     runner()

# if __name__ == "__main__":
#     main()