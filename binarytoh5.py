import numpy as np
import h5py

filein = open("brain.raw", "rb")
fileout = h5py.File('brain.h5', 'w')
arr = np.arange(100)
fileout.create_dataset("data",data=arr,dtype='x.astype(np.int16)')
