"""Functions for downloading and reading MNIST data."""
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import pickle
import glob 
import numpy
from six.moves import xrange  # pylint: disable=redefined-builtin

#from tensorflow.examples.tutorials.tcga import base
import base
from tensorflow.python.framework import dtypes
from tensorflow.python.platform import gfile

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'


def _read32(bytestream):
  dt = numpy.dtype(numpy.uint32).newbyteorder('>')
  return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]


def extract_images(filename):
  """Extract the images into a 4D uint8 numpy array [index, y, x, depth]."""
  print('Extracting', filename)
  with gfile.Open(filename, 'rb') as f, gzip.GzipFile(fileobj=f) as bytestream:
    magic = _read32(bytestream)
    if magic != 2051:
      raise ValueError('Invalid magic number %d in MNIST image file: %s' %
                       (magic, filename))
    num_images = _read32(bytestream)
    rows = _read32(bytestream)
    cols = _read32(bytestream)
    buf = bytestream.read(rows * cols * num_images)
    data = numpy.frombuffer(buf, dtype=numpy.uint8)
    data = data.reshape(num_images, rows, cols, 1)
    return data


def dense_to_one_hot(labels_dense, num_classes):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = numpy.arange(num_labels) * num_classes
  labels_one_hot = numpy.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot


def extract_labels(filename, one_hot=False, num_classes=10):
  """Extract the labels into a 1D uint8 numpy array [index]."""
  print('Extracting', filename)
  with gfile.Open(filename, 'rb') as f, gzip.GzipFile(fileobj=f) as bytestream:
    magic = _read32(bytestream)
    if magic != 2049:
      raise ValueError('Invalid magic number %d in MNIST label file: %s' %
                       (magic, filename))
    num_items = _read32(bytestream)
    buf = bytestream.read(num_items)
    labels = numpy.frombuffer(buf, dtype=numpy.uint8)
    if one_hot:
      return dense_to_one_hot(labels, num_classes)
    return labels


class DataSet(object):

  def __init__(self,
               images,
               labels,
               fake_data=False,
               one_hot=False,
               dtype=dtypes.float32):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.
    """
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    if fake_data:
      self._num_examples = 10000
      self.one_hot = one_hot
    else:
      assert len(images) == len(labels), (
          'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
      self._num_examples = len(images)
      '''
      # Convert shape from [num examples, rows, columns, depth]
      # to [num examples, rows*columns] (assuming depth == 1)
      assert images.shape[3] == 1
      images = images.reshape(images.shape[0],
                              images.shape[1] * images.shape[2])
      if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
      '''
    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size, fake_data=False):
    """Return the next `batch_size` examples from this data set."""
    if fake_data:
      fake_image = [1] * 20502
      if self.one_hot:
        fake_label = [1] + [0] * 33
      else:
        fake_label = 0
      return [fake_image for _ in xrange(batch_size)], [
          fake_label for _ in xrange(batch_size)
      ]
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    if self._index_in_epoch > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Shuffle the data
      perm = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm)
      self._images = self._images[perm]
      self._labels = self._labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size
      assert batch_size <= self._num_examples
    end = self._index_in_epoch
    return self._images[start:end], self._labels[start:end]


def read_data_sets(train_dir,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32):
  if fake_data:

    def fake():
      return DataSet([], [], fake_data=True, one_hot=one_hot, dtype=dtype)

    train = fake()
    validation = fake()
    test = fake()
    return base.Datasets(train=train, validation=validation, test=test)
  normal_const=20502 #To normalize the input value
  #loading training dataset
  train_values=[] #for training dataset values
  train_labels=[] #for training dataset labels
  for file in glob.glob(train_dir+"/*type1*"):
    f=gzip.open(file)
    a=pickle.load(f)
    for i in range(0,len(a[0])):
        train_values.append(a[0][i]/normal_const)
        train_labels.append(a[1][i])
  #print(len(train_dataset_values), len(train_dataset_labels))
  train_values = numpy.array(train_values)
  train_labels = numpy.array(train_labels,numpy.uint16)
  train_labels=train_labels-1#CLASSES [0,NUM_CLASSES)
  train = DataSet(train_values, train_labels, dtype=dtype)
  print("Number of training dataset: %d " %len(train_values))
  #print(train_labels)
  #loading valiation dataset
  validation_values=[] #for training dataset values
  validation_labels=[] #for training dataset labels
  for file in glob.glob(train_dir+"/*type2*"):
    f=gzip.open(file)
    a=pickle.load(f)
    for i in range(0,len(a[0])):
        validation_values.append(a[0][i]/normal_const)
        validation_labels.append(a[1][i])
  #print(len(train_dataset_values), len(train_dataset_labels))
  validation_values = numpy.array(validation_values)
  validation_labels = numpy.array(validation_labels,dtype=numpy.uint16)
  validation_labels = validation_labels-1 #CLASSES [0,NUM_CLASSES)
  validation = DataSet(validation_values, validation_labels, dtype=dtype)
  print("Number of valiation dataset: %d " %len(validation_values))
  #loading test dataset
  test_values=[] #for training dataset values
  test_labels=[] #for training dataset labels
  for file in glob.glob(train_dir+"/*type3*"):
    f=gzip.open(file)
    a=pickle.load(f)
    for i in range(0,len(a[0])):
        test_values.append(a[0][i]/normal_const)
        test_labels.append(a[1][i])
  #print(len(train_dataset_values), len(train_dataset_labels))
  test_values = numpy.array(test_values)
  test_labels = numpy.array(test_labels,dtype=numpy.uint16)
  test_labels = test_labels-1 #CLASSES [0,NUM_CLASSES)
  test = DataSet(test_values, test_labels, dtype=dtype)
  print("Number of test dataset: %d " %len(test_values))
  return base.Datasets(train=train, validation=validation, test=test)

def load_mnist():
  return read_data_sets('MNIST_data')
