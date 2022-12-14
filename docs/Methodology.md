# How to obtain good performance

## Introduction

Here I'll describe the procedure I used to obtain the
[CIFAR-10](http://www.cs.toronto.edu/~kriz/cifar.html) scores mentioned on the
front page. Skip this section if you're just interested in the convolutional net
code, not the details of how the CIFAR-10 scores were obtained.

## Methodology

I'll use the 13% test error score as the example. You can download the [layer
definition file](../example-layers/layers-conv-local-13pct.cfg) and the [layer
parameter file](../example-layers/layer-params-conv-local-13pct.cfg).

We will be training on random 24x24 patches extracted from the 32x32 CIFAR-10
images. You can read a bit more about that
[here](TrainingNet.md#Training_on_image_translations).

We'll be using a version of the CIFAR-10 in which all the data matrices have
been transposed (because that format is convenient for this code). You can
download it [here](http://www.cs.toronto.edu/~kriz/cifar-10-py-colmajor.tar.gz).
It's the same version as is used in [other sections](Data.md) of these docs.

We'll use batches 1-4 for training and batch 5 for validation (early stopping).
Batch 6 of course is the test set.

Start by training the net on batches 1-4 and "testing" on batch 5. Train until
the validation error stops improving. Since I've run this net before, I know
that this happens after roughly 100 epochs. So we start the net with the
parameters `--train-range=1-4`, `--test-range=5`, and `--epochs=100`. Like so:

```sh
python convnet.py \
    --data-path=/storage2/tiny/cifar-10-batches-py-colmajor/ \
    --save-path=/storage2/tmp \
    --test-range=5 \
    --train-range=1-4 \
    --layer-def=./example-layers/layers-conv-local-13pct.cfg \
    --layer-params=./example-layers/layer-params-conv-local-13pct.cfg \
    --data-provider=cifar-cropped \
    --test-freq=13 \
    --crop-border=4 \
    --epochs=100
```

Now note the *training error* after the above run has finished. In this case, it
is roughly 0.4 [nats](https://en.wikipedia.org/wiki/Nat_(information) ):

```
100.2... logprob:  0.418657, 0.145800 (1.857 sec)
100.3... logprob:  0.405222, 0.141100 (1.862 sec)
100.4... logprob:  0.419132, 0.145400 (1.857 sec)
101.1... logprob:  0.394249, 0.137100 (1.855 sec)
```

Now we'll resume training, but this time on all 5 batches of the CIFAR-10
training set. We will stop training when the *training error on batch 5* (which
used to be our validation set) reaches 0.4 nats. Because I have done this
before, I know this takes roughly 40 more epochs. So we run the net like this:

```sh
python convnet.py \
    -f /storage2/tmp/ConvNet__2011-12-17_18.13.52 \
    --train-range=1-5 \
    --epochs=140
```

Now we reduce all learning rates (the `epsW` parameters) in the
[layer parameter file](../example-layers/layer-params-conv-local-13pct.cfg) by a
factor of 10, and train for another 10 epochs:

```sh
python convnet.py \
    -f /storage2/tmp/ConvNet__2011-12-17_18.13.52 \
    --epochs=150
```

Reduce all learning rates in the layer parameter file by *another* factor of 10,
and train for *another* 10 epochs:

```sh
python convnet.py \
    -f /storage2/tmp/ConvNet__2011-12-17_18.13.52 \
    --epochs=160
```

Finally, substitute the real test set, and test on it using the procedure
described [here](TrainingNet.md#training-on-image-translations):

```sh
python convnet.py \
    -f /storage2/tmp/ConvNet__2011-12-17_18.13.52 \
    --multiview-test=1 \
    --test-only=1 \
    --logreg-name=logprob \
    --test-range=6
```

You should see output that looks something like this, in this case indicating a 12.6% test error.

```
======================Test output======================
logprob:  0.423908, 0.126000
```

Notes:

* During step 3, you will see test error printouts that are very low -- this is
  because the net is testing on batch 5, on which it is also training. But it is
  testing on only the *center patches*, while it is training on all patches.
* The test error will of course fluctuate slightly from run to run, so 13% is a
  conservative estimate.
* The total training time in this case is 1.86 seconds x 4 batches x 100 epochs
  + 1.86 seconds x 5 batches x 60 epochs = *21.7 minutes*.
