import cv2
import numpy as np

def clear_noize(img):
    ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    areas = []
    for i in contours:
        areas.append(cv2.contourArea(i))

    ind = areas.index(max(areas))

    for i in range(0, len(contours)):
        if i != ind:
            mask = np.zeros(img.shape, np.uint8)
            cv2.drawContours(mask, [contours[i]], 0, 255, -1)
            pixelpoints = cv2.findNonZero(mask)

            for pixel in pixelpoints:
                img[pixel[0][1], pixel[0][0]] = 0
    return img


def colour_extract(img, colour1L = [0, 120, 70], colour1R = [10, 255, 255],
                        colour2L = [170, 120, 70], colour2R = [180, 255, 255]):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array(colour1L)
    upper_red = np.array(colour1R)

    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array(colour2L)

    upper_red = np.array(colour2R)

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
    return mask1

def extract_gesture(img, L1, R1, L2, R2):

    mask = colour_extract(img, L1, R1, L2, R2)
    mask1 = clear_noize(mask)

    mask = mask1 > 0
    coords = np.argwhere(mask)
    try:
        x0, y0 = coords.min(axis=0)
        x1, y1 = coords.max(axis=0) + 1

        cropped = mask1[x0:x1, y0:y1]
        return cropped, 1
    except:
        return 0, 0