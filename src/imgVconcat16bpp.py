import cv2, glob, os, sys
import numpy as np

def main():

    argv = sys.argv
    argc = len(argv)

    print('%s concatenates images vertivally' % argv[0])
    print('[usage1] python %s <image1> <image2> ...' % argv[0])
    print('[usage2] python %s <wildcard for images>' % argv[0])

    if argc < 2:
        quit()

    Wmax = -1
    imgs = []
    Hs = []
    Ws = []

    if argc > 2:
        for i in range(1, argc):
            img = cv2.imread(argv[i], cv2.IMREAD_UNCHANGED)
            imgs.append(img)
            H, W = img.shape[:2]
            Hs.append(H)
            Ws.append(W)
            if W > Wmax:
                Wmax = W
    else:
        paths = glob.glob(argv[1])
        for path in paths:
            img = cv2.imread(path)
            imgs.append(img)
            H, W = img.shape[:2]
            Hs.append(H)
            Ws.append(W)
            if W > Wmax:
                Wmax = W

    dst = np.zeros((sum(Hs), Wmax), np.uint16)

    nrImages = len(imgs)
    top = 0
    left = 0

    for i in range(nrImages):

        left = (Wmax - Ws[i]) // 2
        right = left + Ws[i]

        bottom = top + Hs[i]

        dst[top:bottom, left:right] = imgs[i]

        top = bottom

    cv2.imwrite('imgVconcat.png', dst)
    print('Save imgVconcat.png')


if __name__ == '__main__':
    main()
