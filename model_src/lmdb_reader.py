import numpy as np
import lmdb,os,sys,math
import matplotlib.pyplot as plt


caffe_root = '/gpu1/adnan/caffe/'  # this file is expected to be in {caffe_root}/examples
sys.path.insert(0, caffe_root + 'python')

import caffe
import caffe.proto.caffe_pb2
from  caffe.io import datum_to_array


LMDB_FILE_NAME = "test_data_lmdb"
LMDB_PATH = os.path.join(os.getcwd(),LMDB_FILE_NAME)
env = lmdb.open(LMDB_PATH, readonly=True, lock=False)

visualize = False
number_of_images = 1
datum = caffe.proto.caffe_pb2.Datum() #datum_pb2.Datum()

with env.begin() as txn:
    cur = txn.cursor()
    
    for i in xrange(number_of_images):
        
        if not cur.next():
            cur.first()
        # Read the current cursor
        key, value = cur.item()
        
        # convert to datum
        datum.ParseFromString(value)
        
        # Read the datum.data
        img_data = datum_to_array(datum)
       
        if visualize:
            plt.imshow(img_data.transpose([1,2,0]))
            plt.show()
        else:
            plt.imsave('sample.png',img_data.transpose([1,2,0]))

        print 'image index in LMDB '+ str(key)