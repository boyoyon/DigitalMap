import glob, sys
import numpy as np

argv = sys.argv
argc = len(argv)

if argc < 2:
    quit()

paths = glob.glob(argv[1])
nrPaths = len(paths)

record = []

for i, path in enumerate(paths):

   print('processing %d/%d: %s' % ((i+1), nrPaths, path))

   data  = np.load(path)    

   code =  data[0] 

   # 経度、緯度を秒単位にする
   top =  data[1] * 3600 + data[2] * 60 + data[3] 
   left =  data[4] * 3600 + data[5] * 60 + data[6] 
   bottom =  data[7] * 3600 + data[8] * 60 + data[9] 
   right =  data[10] * 3600 + data[11] * 60 + data[12] 

   record.append((code, top, left, bottom, right))

layout = np.array(record)
np.save('layout.npy', layout)
print('save layout.npy')