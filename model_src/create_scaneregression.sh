#!/usr/bin/env sh
# This script converts the mnist data into lmdb/leveldb format,
# depending on the value assigned to $BACKEND.

#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs


EXAMPLE=../../examples/scane-regression # location should indicate the caffe project location
DATA=../../data/scane-regression # should locate train.txt,val.txt and test.txt. Currently it's in caffe/data/scane-regression/ **

TOOLS=../../build/tools # should not be changed because by default it uses  convert_imageset to create lmdb dataset.

TRAIN_DATA_ROOT=../../../regression-datasets/train/
VAL_DATA_ROOT=../../../regression-datasets/val/
TEST_DATA_ROOT=../../../regression-datasets/test/

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.

RESIZE=false

if $RESIZE; then
  RESIZE_HEIGHT=256
  RESIZE_WIDTH=256
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_scaneregression.sh to the path" \
       "where the regression training data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_scaneregression.sh to the path" \
       "where the regression validation data is stored."
  exit 1
fi

if [ ! -d "$TEST_DATA_ROOT" ]; then
  echo "Error: TEST_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the TEST_DATA_ROOT variable in create_scaneregression.sh to the path" \
       "where the regression validation data is stored."
  exit 1
fi

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $DATA/train.txt \
    $EXAMPLE/scane_train_lmdb

# echo "Creating val lmdb..."

# GLOG_logtostderr=1 $TOOLS/convert_imageset \
#     --resize_height=$RESIZE_HEIGHT \
#     --resize_width=$RESIZE_WIDTH \
#     --shuffle \
#     $VAL_DATA_ROOT \
#     $DATA/val.txt \
#     $EXAMPLE/scane_val_lmdb

# echo "Creating test lmdb..."

# GLOG_logtostderr=1 $TOOLS/convert_imageset \
#     --resize_height=$RESIZE_HEIGHT \
#     --resize_width=$RESIZE_WIDTH \
#     --shuffle \
#     $VAL_DATA_ROOT \
#     $DATA/test.txt \
#     $EXAMPLE/scane_test_lmdb

echo "Done."
