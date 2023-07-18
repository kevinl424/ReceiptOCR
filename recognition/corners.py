import cv2 as cv
import numpy as np


def apply_filters(img):
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binaryImage = cv.threshold(grayscale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cannyImage = cv.Canny(binaryImage, threshold1=120, threshold2=255, edges=1)
    contours, hierarchy = cv.findContours(cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cv.imshow("image", cannyImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return contours


def convex_hull(contours, orig):
    cornerlist = []
    minThreshold = 100000
    for i, c in enumerate(contours):
        perimeter = cv.arcLength(c, True)
        poly = cv.approxPolyDP(c, 0.02 * perimeter, True)
        bound = cv.boundingRect(poly)
        rectX, rectY, rectWidth, rectHeight = bound[0], bound[1], bound[2], bound[3]
        area = rectHeight * rectWidth

        if area > minThreshold:
            hull = cv.convexHull(c)
            color = (0, 0, 255)
            cv.polylines(orig, [hull], True, color, 2)
            # Create image for good features to track:
            (height, width) = orig.shape[:2]
            # Black image same size as original input:
            hullImg = np.zeros((height, width), dtype =np.uint8)

            # Draw the points:
            cv.drawContours(hullImg, [hull], 0, 255, 2)
            cv.imshow("hullImg", hullImg)
            cv.waitKey(0)

    maxCorners = 4
    qualityLevel = 0.01
    minDistance = int(max(height, width) / maxCorners)

    # Get the corners:
    corners = cv.goodFeaturesToTrack(hullImg, maxCorners, qualityLevel, minDistance)
    corners = np.intp(corners)

    # Loop through the corner array and store/draw the corners:
    for c in corners:

        # Flat the array of corner points:
        (x, y) = c.ravel()
        # Store the corner point in the list:
        cornerlist.append((x,y))

        # (Optional) Draw the corner points:
        cv.circle(orig, (x, y), 5, 255, 5)
        cv.imshow("Corners", orig)
        cv.waitKey(0)
    cv.destroyAllWindows()
    return corners

def main(path):
    img = cv.imread(path)
    contours = apply_filters(img)
    corners = convex_hull(contours, img)
    return corners

if __name__=="__main__":
    main()
