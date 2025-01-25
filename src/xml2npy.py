import glob, os, re, sys
import numpy as np

WIDTH = 225
HEIGHT = 150

def fixup(heightmap):

    height, width = heightmap.shape[:2]

    for y in range(height):
        for x in range(width):
            if heightmap[y][x] < 0:
                total = 0
                count = 0

                if y > 0:
                    north = heightmap[y-1][x]
                    if north >= 0:
                        total += north
                        count += 1

                if y < height - 1:
                    south = heightmap[y+1][x]
                    if south >= 0:
                        total += south
                        count += 1

                if x > 0:
                    west = heightmap[y][x-1]
                    if west >= 0:
                        total += west
                        count += 1

                if x < width - 1:
                    east = heightmap[y][x+1]
                    if east >= 0:
                        total += east
                        count += 1

                heightmap[y][x] = total // count

argv = sys.argv
argc = len(argv)

print('%s converts xmls to npy' % argv[0])
print('[usage] python %s <wildcard for xml>' % argv[0])

if argc < 2:
    quit()

paths = glob.glob(argv[1])

for path in paths:

    base = os.path.basename(path)

    filename = re.sub("FG-GML-[0-9]*-[0-9]*-", "", base)
    filename = re.sub("-.*", "", filename) 

    dst_path = '%s.npy' % filename

    with open(path, mode='r', encoding='utf-8-sig') as f:
        lines = f.read().split('\n')

    heightmap = []
    lineNo = 1
    dataenable = False

    for line in lines:

        if line == '<gml:tupleList>':
            dataenable = True
            continue

        if line == '</gml:tupleList>':
            dataenable = False
            continue

        if dataenable:
            data = line.split(',')

            try:
                height = float(data[1])

            except ValueError:
                #print('Failed: %s at %d' % (line, lineNo))
                continue

            heightmap.append(height)
            lineNo += 1

    heightmap = np.array(heightmap, dtype=np.float32)

    heightmap = heightmap.reshape((HEIGHT, WIDTH))

    fixup(heightmap)

    np.save(dst_path, heightmap)

    print('save %s' % dst_path)
