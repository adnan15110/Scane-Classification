import numpy as np
import lmdb,os,sys,math

caffe_root = '/gpu1/adnan/caffe/'
sys.path.insert(0, caffe_root + 'python')

import caffe


class CreateLmdb:
	def __init__(self):
		# configure below variables
		# location to the folder where the raw image file located
		self.dataset_path = os.path.join("..","..","..","..","regression-datasets")
		# location to the folder where the train.txt, test.txt and val.txt located
		self.txt_file_path = os.path.join("..","..","..","..","regression-datasets")

		dataset_type = ['test']

		for d_type in dataset_type:
		    self.create_lmdb_file(d_type)

	def create_images_labels_list(self, dataset_type):
		images = []
		labels = []
		f = open(os.path.join(self.txt_file_path, dataset_type+'.txt'))

		for line in f.readlines():
			image,label = line.strip().split(' ')
			image_location = os.path.join(self.dataset_path,dataset_type,image)
			images.append(image_location)
			labels.append(float(label))

		return images, labels

	def create_lmdb_file(self, dataset_type):

		print 'Writing LMDB data ...'

		lmdb_data_name = dataset_type + '_data_lmdb'
		lmdb_label_name = dataset_type + '_score_lmdb'


		images,labels = self.create_images_labels_list(dataset_type)
		print 'Writing labels ...'

		# Size of buffer: 1000 elements to reduce memory consumption

		for idx in range(int(math.ceil(len(labels)/1000.0))):
			in_db_label = lmdb.open(lmdb_label_name, map_size=int(1e12))
			with in_db_label.begin(write=True) as in_txn:
				for label_idx, label_ in enumerate(labels[(1000*idx):(1000*(idx+1))]):
					im_dat = caffe.io.array_to_datum(np.array(label_).astype(float).reshape(1,1,1))
					in_txn.put('{:0>10d}'.format(1000*idx + label_idx), im_dat.SerializeToString())
					string_ = str(1000*idx+label_idx+1) + ' / ' + str(len(labels))
					sys.stdout.write("\r%s" % string_)
					sys.stdout.flush()
			in_db_label.close()

		print '\nfinished'

		print 'Writing image data'

		for idx in range(int(math.ceil(len(images)/1000.0))):
			in_db_data = lmdb.open(lmdb_data_name, map_size=int(1e12))
			with in_db_data.begin(write=True) as in_txn:
				for in_idx, in_ in enumerate(images[(1000*idx):(1000*(idx+1))]):
					im = caffe.io.load_image(in_)
					im_dat = caffe.io.array_to_datum(im.astype(float).transpose((2, 0, 1)))
					in_txn.put('{:0>10d}'.format(1000*idx + in_idx), im_dat.SerializeToString())

					string_ = str(1000*idx+in_idx+1) + ' / ' + str(len(images))
					sys.stdout.write("\r%s" % string_)
					sys.stdout.flush()
			in_db_data.close()
		print '\nfinished'


if __name__ == '__main__':
	create_lmdb = CreateLmdb()
