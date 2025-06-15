import cv2, glob, os, sys
import numpy as np

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s concatenates images horizontally' % argv[0])
    print('[usage1] python %s <image1> <image2> ...' % argv[0])
    print('[usage2] python %s <wildcard for images>' % argv[0])

    if argc < 2:
        quit()

    Hmax = -1
    imgs = []
    Hs = []
    Ws = []

    if argc > 2:
        for i in range(1, argc):
            img = cv2.imread(argv[i],cv2.IMREAD_UNCHANGED)
            imgs.append(img)
            H, W = img.shape[:2]
            Hs.append(H)
            Ws.append(W)
            if H > Hmax:
                Hmax = H
    else:
        paths = glob.glob(argv[1])
        for path in paths:
            img = cv2.imread(path)
            imgs.append(img)
            H, W = img.shape[:2]
            Hs.append(H)
            Ws.append(W)
            if H > Hmax:
                Hmax = H

    dst = np.zeros((Hmax, sum(Ws)), np.uint16)
    #dst = np.ones((Hmax, sum(Ws), 3), np.uint8)
    #dst *= 255

    nrImages = len(imgs)
    top = 0
    left = 0

    for i in range(nrImages):

        right = left + Ws[i]

        top = (Hmax - Hs[i]) // 2
        bottom = top + Hs[i]

        dst[top:bottom, left:right] = imgs[i]

        left = right

    cv2.imwrite('imgHconcat.png', dst)
    print('Save imgHconcat.png')


if __name__ == '__main__':
    main()
