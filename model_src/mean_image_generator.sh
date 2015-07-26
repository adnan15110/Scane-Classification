#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

EXAMPLE=../../examples/scane-regression # location should indicate the caffe project location
DATA=../../data/scane-regression # should locate train.txt,val.txt and test.txt. Currently it's in caffe/data/scane-regression/ **

TOOLS=../../build/tools # should not be changed because by default it uses  compute_image_mean to create lmdb dataset.

$TOOLS/compute_image_mean $EXAMPLE/train_data_lmdb \
  $EXAMPLE/image_mean.binaryproto

echo "Done."
