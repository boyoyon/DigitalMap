"""
depth2ply.py
テクスチャー座標無しバージョン

"""

import cv2, os, sys
import numpy as np

def read_depth(depth_image, zScale, zTh):

    positions = []
    faces = []

    if len(depth_image.shape) > 2:
        depth_image = cv2.split(depth_image)[0]

    height, width = depth_image.shape[:2]

    aspect = width / height

    depth_max = np.max(depth_image)
    depth_mean = np.mean(depth_image)
    depth_th = depth_mean * zTh

    for y in range(height):

        for x in range(width):

            d = depth_image[y][x]

            positions.append(((x/width - 0.5) * aspect, y/height - 0.5, (0.5 - d/depth_max) * zScale))
    
            if y < height - 1 and x < width - 1 and d > depth_th:

                idx0 = y * width + x
                idx1 = y * width + x + 1
                idx2 = (y + 1) * width + x
                idx3 = (y + 1) * width + x + 1
    
                faces.append((idx0, idx3, idx1))
                faces.append((idx0, idx2, idx3))

    return positions, faces

def Depth2ply(ply_filename, positions, faces, flag = 0):

    with open(ply_filename, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % len(positions)
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'element face %d\n' % len(faces)
        f.write(line)

        #line = 'property list uchar int vertex_index\n'
        line = 'property list uchar int vertex_indices\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for i in range(len(positions)):
            line = '%f %f %f\n' % (positions[i][0], positions[i][1], positions[i][2])
            f.write(line)

        for i in range(len(faces)):
            idx0 = faces[i][0]
            idx1 = faces[i][1]
            idx2 = faces[i][2]
            
            if flag == 0:
                line = '3 %d %d %d\n' % (idx0, idx1, idx2)
            else:
                line = '3 %d %d %d\n' % (idx0, idx2, idx1)
            
            f.write(line)

def main():

    zScale = 1.0
    zTh = 0.0

    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        print('%s creates ply from a depth' % argv[0])
        print('[usage] python %s <depth image> [<zScale> <flag>]' % argv[0])
        quit()

    depth_path = argv[1]
    base = os.path.basename(depth_path)
    filename, _ = os.path.splitext(base)

    if argc > 2:
        zScale = float(argv[2])

    flag = 0
    if argc > 3:
        flag = int(argv[3])

    depth_image = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
    positions, faces = read_depth(depth_image, zScale, zTh)

    ply_filename = '%s.ply' % filename

    Depth2ply(ply_filename, positions, faces, flag)

if __name__ == "__main__":
    main()
