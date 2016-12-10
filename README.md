# caffe-Scane-classification model

This code creates dataset to feed into caffe for classification.

How to run it

step 1: creating the train/test/validation dataset. Follow below structure:
  datasets-
    -train
    -test
    -validation
  

use dataset_creator.py to generate these folders. dataset_creator.py also creates train.txt, test.txt, validation.txt, these file will be used in the next step to create lmdb dataset (used in caffe models). train.txt, test.txt and validation.txt moved to caffe/data/scane-regression folder.

step 2: create lmdb dataset for caffe models
      - create/modify create_scaneregression.sh [need to be uploaded]
      - check comments to modify path such as "datasets" location
      - execute create_scaneregression.sh
       - ./create_scaneregression.sh
       
       this step will create lmdb files for model training. lmdb files will be stored in caffe/example/scane-regression folder.
