import glob, sys
import numpy as np

argv = sys.argv
argc = len(argv)

if argc < 2:
    print('%s concatenates npy vertically' % argv[0])
    print('[usage] python %s <npy1> <npy2> ....' % argv[0])
    print('[usage] python %s <wildcard for .npy>' % argv[0])
    quit()

paths = []

if argc > 2:
    for i in range(1, argc):
        paths.append(argv[i])

else:
    paths = glob.glob(argv[1])

nrData = len(paths)

block0 = np.load(paths[0])
block0 = np.flipud(block0)

print('processing 1/%d: %s' % (nrData, paths[0]))

for i in range(1, nrData):
    print('processing %d/%d: %s' % ((i+1), nrData, paths[i]))

    block = np.load(paths[i])
    block = np.flipud(block)
    
    block0 = np.vstack((block0, block))

np.save('vstack.npy', block0)
print('save vtsack.npy')
