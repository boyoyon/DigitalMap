import cv2, sys
import numpy as np

SCALE = 70

# layout.npy
#   各MEMファイルに収められた左上緯度経度、右下緯度経度
#   集めた numpy ファイル
#
record = np.load('layout.npy')

CODE = record[:,0]

TOP = record[:,1]
SORTED_TOP = np.unique(np.sort(TOP))
SORTED_TOP = SORTED_TOP[::-1]
R = SORTED_TOP.shape[0]

LEFT = record[:,2]
SORTED_LEFT = np.unique(np.sort(LEFT))
C = SORTED_LEFT.shape[0]

screen = np.ones((R*SCALE, C*SCALE, 3), np.uint8)
screen *= 255

font = cv2.FONT_HERSHEY_PLAIN
font_size = 1
font_color = (0, 0, 255)

for r, top in enumerate(SORTED_TOP):

    print('%d/%d' % ((r+1), R))

    indicesT = np.where(TOP == top)[0]

    for c, left in enumerate(SORTED_LEFT):

        cv2.rectangle(screen, (c * SCALE, r * SCALE), ((c+1)*SCALE, (r+1)*SCALE), (0, 0, 255), 1)

        indicesL = np.where(LEFT == left)[0]

        commonIdx = np.intersect1d(indicesT, indicesL)

        if commonIdx.size == 0:
            continue

        else:
            idx = commonIdx[0]

            top = r * SCALE
            bottom = top + SCALE

            left = c * SCALE
            right = left + SCALE

            str = '%d' % CODE[idx]


            cv2.putText(screen, str, (left+5, top+SCALE//2), font, font_size, font_color, 2)

cv2.imwrite('layout.png', screen) 


