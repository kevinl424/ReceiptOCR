import pytesseract
import cv2 as cv
import numpy as np
import re
import imutils
from skimage.filters import threshold_local
from scipy.ndimage import rotate


def skew_correction(img, delta=0.05, limit=5):
    # convert to binary image first
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.bitwise_not(gray)
    thresh = cv.threshold(gray, 0, 255,
	    cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    
    # scores = []
    # angles = np.arange(-limit, limit + delta, delta)

    # def hist(angle):
    #     data = rotate(thresh, angle, reshape=False, order=0)
    #     histogram = np.sum(data, axis=1, dtype=float)
    #     score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
    #     return histogram, score

    # for angle in angles:
    #     (histogram, score) = hist(angle)
    #     scores.append(score)
    
    # best = angles[scores.index(max(scores))]
    # h, w = img.shape[:2]
    # center = (w // 2, h // 2)

    # matrix = cv.getRotationMatrix2D(center, best, 1.0)
    # corrected = cv.warpAffine(img, matrix, (w, h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    # return corrected

    coords = np.column_stack(np.where(thresh > 0))
    angle = cv.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv.warpAffine(img, M, (w, h),
	flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
    cv.putText(rotated, "Angle: {:.2f} degrees".format(angle),
	(10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    cv.imshow("Input", img)
    cv.imshow("Rotated", rotated)
    cv.waitKey(0)



# apply visual filters to transformed image
def filter_img(img):
    edit = cv.threshold(img, 127, 255, cv.THRESH_OTSU)[1]
    edit = cv.medianBlur(edit, 3)

    # testing these methods for now

    # kernal = np.ones((5,5), np.uint8)
    # edit = cv.erode(edit, kernal, iterations = 1)
    # edit = cv.dilate(edit, kernal, iterations = 1)
    
    # show for testing
    # cv.imshow("filtered_img", edit)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    return edit


# ordering points for transform
def order_points(pts):
    reordered = np.zeros((4, 2), dtype="float32")
    sums = pts.sum(axis=1) # sum along horizontal axis

    reordered[0] = pts[np.argmin(sums)]
    reordered[2] = pts[np.argmax(sums)]

    diffs = np.diff(pts, axis=1)
    reordered[1] = pts[np.argmin(diffs)]
    reordered[3] = pts[np.argmax(diffs)]
    return reordered


# perform transform
def four_point_transform(img, pts):
    original = order_points(pts)
    (tl, tr, bl, br) = original

    # use pyth theorem to calc width and height
    width1 = np.sqrt(((tr[0] - tl[0]) ** 2) + (tr[1] - tl[1]) ** 2)
    width2 = np.sqrt(((br[0] - bl[0]) ** 2) + (br[1] - bl[1]) ** 2)
    width = max(int(width1), int(width2))

    height1 = np.sqrt(((tr[0] - br[0]) ** 2) + (tr[1] - br[1]) ** 2)
    height2 = np.sqrt(((tl[0] - bl[0]) ** 2) + (tl[1] - bl[1]) ** 2)
    height = max(int(height1), int(height2))

    change = np.array(
        [[0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype="float32"
    )
    matrix = cv.getPerspectiveTransform(original, change)
    new = cv.warpPerspective(img, matrix, (width, height))
    return new


# create rectangle that encompasses all points
def trim_points(contour):
    # numpy.array([[1,1],[10,50],[50,50]], dtype=numpy.int32

    points = np.squeeze(contour)
    x = points[:, 0]
    y = points[:, 1]

    topy, leftx = np.min(y), np.min(x)
    bottomy, rightx = np.max(y), np.max(x)
    tl = [leftx, topy]
    tr = [rightx, topy]
    br = [rightx, bottomy]
    bl = [leftx, bottomy]

    retCnt = np.array([[tl, tr, br, bl]], dtype=np.int32)
    return retCnt


# finds contours and calls transform
def perspectiveTransform(path):
    img = cv.imread(path)
    ratio = img.shape[0] / 500
    orig = img.copy()
    img = imutils.resize(img, height=500)

    edit = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edit = cv.GaussianBlur(edit, (5, 5), 0)
    edit = cv.Canny(edit, 75, 200)

    # cv.imshow("edited_img", edit)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    contours = cv.findContours(edit.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv.contourArea, reverse=True) # sort by contour area with largest first
    contours = contours[:5] # only take the largest to examine

    # sort by descending perimter
    contours.sort(key=lambda c:cv.arcLength(c, True))

    for c in contours:
        perimeter = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * perimeter, True)
        
        if len(approx) > 4:
            # trim necessary to find four outstanding points
            retCnt = trim_points(approx)
        elif len(approx) == 4:
            retCnt = approx
            break

    cv.drawContours(img, [retCnt], -1, (0, 225, 0), 2)
    # cv.imshow("find_corners", img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    warped = four_point_transform(orig, retCnt.reshape(4, 2) * ratio)
    warped = cv.cvtColor(warped, cv.COLOR_BGR2GRAY)
    T = threshold_local(warped, block_size=21, offset = 8, method = "gaussian")
    # pixels that exceed threshold, aka foreground (text)
    warped = (warped > T).astype("uint8") * 255
    imutils.resize(warped, height = 650)

    # cv.imshow("finished_img", warped)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return warped

if __name__=="__main__":
    img = cv.imread("recognition/test_images/skew.png")
    cv.imshow("original", img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    corrected = skew_correction(img)
    cv.imshow("corrected", corrected)
    cv.waitKey(0)
    cv.destroyAllWindows()