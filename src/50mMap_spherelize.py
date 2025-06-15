import cv2, sys
import numpy as np

BIAS = 65535 // 2
R = 6378000 #地球の半径 (単位 m)

argv = sys.argv
argc = len(argv)

print('%s spherelize depth map' % argv[0])
print('[usage] python %s <depthmap>' % argv[0])

if argc < 2:
    quit()

depth = cv2.imread(argv[1], cv2.IMREAD_UNCHANGED)
depth += BIAS

height = depth.shape[0]
width = depth.shape[1]

cx = width // 2
cy = height // 2

for y in range(height):
    print('processing %d/%d' % ((y+1), height))

    for x in range(width):
        l = np.sqrt((x -cx) ** 2 + (y - cy) ** 2)
        theta = l * 50 / R # 1ピクセルが50mの場合
        correction = int(R*(1 - np.cos(theta)))

        depth[y][x] -= correction

cv2.imwrite('map_spherized.png', depth)


