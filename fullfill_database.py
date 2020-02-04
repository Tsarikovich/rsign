import cv2
import numpy as np
import segmentation as seg
import os

def create_static(path, end, l1, r1, l2, r2, imgsize = 224):
    imageSize = 224

    cap = cv2.VideoCapture(0)
    count, background = 0, 0

    for i in range(60):
        ret, background = cap.read()
    i = 0

    while (cap.isOpened()):
        try:
            ret, img = cap.read()

            if not ret:
                break

            count += 1

            img = seg.extract_gesture(l1, r1, l2, r2, img)

            cv2.imshow('Img', img)
            k = cv2.waitKey(10)

            if k == 32:
                img = cv2.resize(img, (imgsize, imgsize))
                path = path + str(i) + ".jpg"
                pl = cv2.imwrite(path, img)
                print(i, 'Added', pl, path)
                i += 1
                if i == end:
                    break
        except:
            pass

def create_dinamic(path, end, l1, r1, l2, r2, imgsize = 50):
    cap = cv2.VideoCapture(0)
    count, background = 0, 0

    for i in range(60):
        ret, background = cap.read()

    i, j, ok = 0, 0, 0

    while (cap.isOpened()):
        try:
            ret, img = cap.read()

            if not ret:
                break

            count += 1

            img = seg.extract_gesture(l1, r1, l2, r2, img)

            cv2.imshow('Img', img)

            if ok == 1:
                j += 1
                img = cv2.resize(img, (imgsize, imgsize))

                try:
                    os.makedirs(path + str(i) + '/')
                except FileExistsError:
                    pass

                cv2.imwrite(path + str(i) + '/' + str(j) + '.jpg', img)

            k = cv2.waitKey(10)

            if k == 49:
                i = i + 1
                j = 0

                print("Recording", i)
                ok = 1

            if k == 50:
                print("Recording", i, "has ended")
                ok = 0

        except:
            pass