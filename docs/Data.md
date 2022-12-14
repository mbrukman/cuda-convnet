# Data format for the net

## Introduction

This code is capable of training on images of any (square) size, and with any number of channels (colors, if you like).

## Data files

The net expects data to be stored as python pickled objects. You can find some
example data
[here](http://www.cs.toronto.edu/~kriz/cifar-10-py-colmajor.tar.gz). This is the
CIFAR-10 dataset.

The data must be broken down into batches. For example, the data above is broken
down into 6 batches of 10000 cases:

```
ls -al /storage2/tiny/cifar-10-py-colmajor
total 181892
drwxr-xr-x  2 spoon spoon     4096 2011-06-26 13:19 .
drwxr-xr-x 34 spoon spoon     4096 2011-06-29 21:40 ..
-rw-r--r--  1 spoon spoon    12583 2011-06-26 13:21 batches.meta
-rw-r--r--  1 spoon spoon 31035679 2011-06-26 13:20 data_batch_1
-rw-r--r--  1 spoon spoon 31035295 2011-06-26 13:20 data_batch_2
-rw-r--r--  1 spoon spoon 31035974 2011-06-26 13:20 data_batch_3
-rw-r--r--  1 spoon spoon 31035671 2011-06-26 13:20 data_batch_4
-rw-r--r--  1 spoon spoon 31035598 2011-06-26 13:20 data_batch_5
-rw-r--r--  1 spoon spoon 31035501 2011-06-26 13:20 data_batch_6
```

Ideally, your test/validation data should be in a separate file from the other files. Here batch 6 is the test set.

Inside the [`util.cuh`](../include/util.cuh) file, there's this line:

```c
/*
 * Store entire data matrix on GPU if its size does not exceed this many MB.
 * Otherwise store only one minibatch at a time.
 */
#define MAX_DATA_ON_GPU             200
```

So, if your batch size isn't too big, it will correspond to the amount of data
copied to the GPU at a time. Otherwise only one minibatch will be copied at a
time, and the batch size will not have much meaning at all.

## Internal data layout

Here you have some freedom. The internals of the files are left up to you; you
just have to write a data provider (a python class) to parse the files and
return the data in a format that the model will understand. See
[`convdata.py`](../convdata.py) for some examples.

Keeping in mind the example of `CIFARDataProvider` in
[`convdata.py`](../convdata.py), you can see that the data provider defines a
`get_next_batch` function which returns a data matrix and a labels vector. There
are a few other constraints on the data provider:

* The data provider must define a function `get_data_dims(self, idx=0)`, which
  returns the data dimensionality of each matrix returned by `get_next_batch`.
* The data matrix must be C-ordered (this is the default for numpy arrays), with
  dimensions `(data dimensionality)x(number of cases)`. If your images have
  channels (for example, the 3 color channels in the CIFAR-10), then all the
  values for channel `n` must precede all the values for channel `n + 1`.
* The data matrix must consist of *single-precision floats*.

Assuming you're going to use the logistic regression objective built into the
code rather than write your own, there are a few additional constraints on the
data provider:

* The labels vector (returned by `get_next_batch`) must have dimensionality
  `1x(number of cases)`.
* The elements of the labels vector must range from 0 until the number of
  classes minus one.
* The labels vector must consist of *single-precision floats*.
* The data provider must define a function `get_num_classes(self)` which simply
  returns the number of classes in your dataset. The `CIFARDataProvider`
  inherits this function from `LabeledDataProvider` defined in
  [`data.py`](../data.py).

Aside from that, there isn't much to trip over.

## Included data providers

This code ships with three data providers. You can find them all in
[`convdata.py`](../convdata.py).

* `CIFARDataProvider` is used to parse the CIFAR-10 dataset. See [training
  net](TrainingNet.md) for details.
* `CroppedCifarDataProvider` is used to parse and crop the CIFAR-10 dataset.
  This is useful if you want to train on translations of the CIFAR-10 images.
  See [training net](TrainingNet.md#Training_on_image_translations) for details.
* `DummyConvNetDataProvider` is used to generate dummy data for gradient-testing
  computations. See [checking gradients](CheckingGradients.md) for details.

Once you've written a new data provider to parse your data, you can register it
at the bottom of the [`convnet.py`](../convnet.py) file with the
`DataProvider.register_data_provider` function, as shown there.
