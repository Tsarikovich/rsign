import cv2
def create_gesture(mas, imgsize):
    a = 0
    for i in mas:
        a += cv2.resize(i, (imgsize,imgsize))
    return a