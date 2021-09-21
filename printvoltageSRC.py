import math
import numpy
import h5py


for j in range (1,50):
  FileName = "sim3d_batch" + str(j) + ".out"
  f = h5py.File(FileName)

  for key, src in f['srcs'].items():
    #name = src.attrs['Name']
    position = src.attrs['Position']
    type = src.attrs['Type']
    ObjectString = type + "  " + FileName
    #print(type)
    print(ObjectString)
    print(position)
    print('\n')
