import cv2, os, sys
import numpy as np

xyScale = 5.0

def main():

    global zScale

    argv = sys.argv
    argc = len(argv)

    print('%s creates ply from a heightmap(npy)' % argv[0])
    print('%s <npy>' % argv[0])
    
    if argc < 2:
        quit()

    heightmap_path = argv[1]
    base = os.path.basename(heightmap_path)
    filename, _ = os.path.splitext(base)
    ply_filename = '%s.ply' % filename

    heightmap = np.load(heightmap_path)

    height, width = heightmap.shape[:2]

    nrVertices = width * height
    nrFaces = (width - 1) * (height - 1) * 2

    shiftX = width / 2
    shiftY = height / 2

    with open(ply_filename, mode='w') as f:

        line = 'ply\n'
        f.write(line)

        line = 'format ascii 1.0\n'
        f.write(line)

        line = 'element vertex %d\n' % nrVertices
        f.write(line)

        line = 'property float x\n'
        f.write(line)

        line = 'property float y\n'
        f.write(line)

        line = 'property float z\n'
        f.write(line)

        line = 'element face %d\n' % nrFaces
        f.write(line)

        line = 'property list uchar int vertex_index\n'
        f.write(line)

        line = 'end_header\n'
        f.write(line)

        for y in range(height):
            yy = (y - shiftY) * xyScale
            for x in range(width):
                xx = (x - shiftX) * xyScale
                z = heightmap[y][x]

                line = '%f %f %f\n' % (xx/1000, yy/1000, z/1000)
                f.write(line)

        for y in range(height - 1):
            for x in range(width - 1):
                idx1 = y * width + x
                idx2 = y * width + x + 1
                idx3 = (y + 1) * width + x
                idx4 = (y + 1) * width + x + 1

                line = '3 %d %d %d\n' % (idx1, idx2, idx4)
                f.write(line)

                line = '3 %d %d %d\n' % (idx1, idx4, idx3)
                f.write(line)

    print('save %s' % ply_filename)

if __name__ == "__main__":
    main()
