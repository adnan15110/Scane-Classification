import numpy as np
from data_reader import DataReader
import os,shutil
from dataset_creator import trainTestandValidationDataCreator

# shutil.copyfile(os.path.join(os.getcwd(),'labels.txt'),\
# 	os.path.join(os.getcwd(),'labels-bak.txt'))

t_class = trainTestandValidationDataCreator()
t_class.createDatasetForRegression()


# d = DataReader('dataset.csv')
# d.csvReader()