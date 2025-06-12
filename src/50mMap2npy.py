import cv2, glob, os, sys
import numpy as np

MAP_HEIGHT = 200
MAP_WIDTH = 200
SKIP2LATITUDE = 23
SKIP2RECORD = 954
SKIP2HEIGHT = 9
SKIP2NEXTREC = 2

SIZE_MESH_CODE = 6
SIZE_DEG = 3
SIZE_MIN = 2
SIZE_SEC = 2
SIZE_HEIGHT = 5

def bcd_to_int(bcd_bytes):
    result = 0

    for i, byte in enumerate(bcd_bytes):
        result *= 10

        if i == 0 and byte == 0x2D:
            result = 0
            break

        else:
            result += byte - 0x30

    return result

def read_mem(path):

    pos = []
    height = []

    with open(path, mode='rb') as f:

       # メッシュコード
       bcd_data = f.read(SIZE_MESH_CODE)
       pos.append(bcd_to_int(bcd_data))

       skipped = f.read(SKIP2LATITUDE)

       # 左上緯度
       bcd_data = f.read(SIZE_DEG)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_MIN)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_SEC)
       pos.append(bcd_to_int(bcd_data))

       # 左上経度
       bcd_data = f.read(SIZE_DEG)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_MIN)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_SEC)
       pos.append(bcd_to_int(bcd_data))

       # 右下緯度
       bcd_data = f.read(SIZE_DEG)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_MIN)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_SEC)
       pos.append(bcd_to_int(bcd_data))

       # 右下経度
       bcd_data = f.read(SIZE_DEG)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_MIN)
       pos.append(bcd_to_int(bcd_data))
       bcd_data = f.read(SIZE_SEC)
       pos.append(bcd_to_int(bcd_data))

       skipped = f.read(SKIP2RECORD)

       for y in range(MAP_HEIGHT):
           skipped = f.read(SKIP2HEIGHT)

           for x in range(MAP_WIDTH):
               bcd_data = f.read(SIZE_HEIGHT)
               height.append(bcd_to_int(bcd_data))

           skipped = f.read(SKIP2NEXTREC)

    return np.array(pos), np.array(height) * 0.1

argv = sys.argv
argc = len(argv)

print('%s converts mem to npy' % argv[0])
print('[usage] python %s <wildcard for MEM>' % argv[0])

if argc < 2:
    quit()

paths = glob.glob(argv[1], recursive=True)

for path in paths:

    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    height_path = '%s.npy' % filename    
    pos_path = '%s_pos.npy' % filename
    img_path = '%s.png' % filename

    pos, height = read_mem(path)
 
    np.save(height_path, height)
    print('save %s' % height_path)

    np.save(pos_path, pos)
    print('save %s' % pos_path)
    print(pos)

    img = height.astype(np.uint16)
    img = np.reshape(img, (200,200))
    cv2.imwrite(img_path, img)
    print('save %s' % img_path)
