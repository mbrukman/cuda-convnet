# How to train a neural net with this code

**Important:** The convolution routines in this code are optimized _only_ for
minibatch sizes which are divisible by 128. Other minibatch sizes will work, but
I made no attempt to make them work fast.

The minibatch size is controlled by the `--mini` parameter (see below). Its
default value is 128, which is optimal from the point of view of the convolution
routines. So my suggestion is to leave it at its default.

## Training

Once you've [compiled](Compiling.md) the code, created a [layer definition
file](LayerParams.md), and found some [data](Data.md) to train on, you can
actually do some training.

Start by typing:

```sh
python convnet.py
```

You should get the following output:

```
convnet.py usage:
    Option                             Description                                          Default
    [--check-grads <0/1>           ] - Check gradients and quit?                            [0]
    [--conv-to-local <string,...>  ] - Convert given conv layers to unshared local          []
    [--crop-border <int>           ] - Cropped DP: crop border size                         [4]
    [--epochs <int>                ] - Number of epochs                                     [50000]
    [-f <string>                   ] - Load file                                            []
    [--gpu <int,...>               ] - GPU override                                         []
    [--logreg-name <string>        ] - Cropped DP: logreg layer name (for --multiview-test) []
    [--max-filesize <int>          ] - Maximum save file size (MB)                          [0]
    [--mini <int>                  ] - Minibatch size                                       [128]
    [--multiview-test <0/1>        ] - Cropped DP: test on multiple patches?                [0]
    [--num-gpus <int>              ] - Number of GPUs                                       [1]
    [--test-freq <int>             ] - Testing frequency                                    [50]
    [--test-one <0/1>              ] - Test on one batch at a time?                         [1]
    [--test-only <0/1>             ] - Test and quit?                                       [0]
    [--unshare-weights <string,...>] - Unshare weight matrices in given layers              []
    [--zip-save <0/1>              ] - Compress checkpoints?                                [0]
     --data-path <string>            - Data path
     --data-provider <string>        - Data provider
     --layer-def <string>            - Layer definition file
     --layer-params <string>         - Layer parameter file
     --save-path <string>            - Save path
     --test-range <int[-int]>        - Data batch range: testing
     --train-range <int[-int]>       - Data batch range: training
```

You can read about the meanings of these options [here](Options.md).

You see that you need to provide a data path, a save (checkpointing) path, some
parameters to do with which chunks to train on and which chunks to test on, and
the layer definition files described [here](LayerParams.md).

The data for this example will be the CIFAR-10 dataset, which you can download
[here](http://www.cs.toronto.edu/~kriz/cifar-10-py-colmajor.tar.gz). If you're
not familiar with the CIFAR-10, you can read about it
[here](http://www.cs.toronto.edu/~kriz/cifar.html). We'll use one of the example
layer configuration files provided in the
[`../example-layers`](../example-layers) subdirectory.

Try this line, replacing the data and save paths with ones that make sense on your system:

```sh
python convnet.py \
    --data-path=/storage2/tiny/cifar-10-batches-py-colmajor/ \
    --save-path=/storage2/tmp \
    --test-range=6 \
    --train-range=1-5 \
    --layer-def=./example-layers/layers-19pct.cfg \
    --layer-params=./example-layers/layer-params-19pct.cfg \
    --data-provider=cifar \
    --test-freq=13
```

This will cause the net to train on data located in
`/storage2/tiny/cifar-10-batches-py-colmajor/` and save checkpoints to
`/storage2/tmp`. It will use batches 1-5 for training and batch 6 for testing.
For every 13 training batches it processes, it will compute the test error once.
The testing frequency is also the checkpoint saving frequency (read more about
this below).

Once the net is running, it will start producing output:

```
Initialized data layer 'data', producing 3072 outputs
Initialized data layer 'labels', producing 1 outputs
Initialized convolutional layer 'conv1', producing 1 groups of 32x32 32-channel output
Initialized max-pooling layer 'pool1', producing 16x16 32-channel output
Initialized convolutional layer 'conv2', producing 1 groups of 16x16 32-channel output
Initialized avg-pooling layer 'pool2', producing 8x8 32-channel output
Initialized convolutional layer 'conv3', producing 1 groups of 8x8 64-channel output
Initialized avg-pooling layer 'pool3', producing 4x4 64-channel output
Initialized fully-connected layer 'fc10', producing 10 outputs
Initialized softmax layer 'probs', producing 10 outputs
Initialized logistic regression cost 'logprob'
```

This just tells you the dimensions of all the layers inside your net. Since we
never _explicitly_ defined how many outputs each convolutional/pooling layer
has, this is good to know.

Then this:

```
Check gradients and quit?            : 0   [DEFAULT]
Compress checkpoints?                : 0   [DEFAULT]
Cropped DP: crop border size         : 4   [DEFAULT]
Cropped DP: logreg layer name        :     [DEFAULT]
Cropped DP: test on multiple patches?: 0   [DEFAULT]
Data batch range: testing            : 6-6
Data batch range: training           : 1-5
Data path                            : /storage2/tiny/cifar-10-batches-py-colmajor/
Data provider                        : cifar
GPU override                         :     [DEFAULT]
Layer definition file                : ./example-layers/layers-19pct.cfg
Layer parameter file                 : ./example-layers/layer-params-19pct.cfg
Load file                            :     [DEFAULT]
Maximum save file size (MB)          : 0   [DEFAULT]
Minibatch size                       : 128 [DEFAULT]
Number of GPUs                       : 1   [DEFAULT]
Number of epochs                     : 300
Save path                            : /storage2/tmp
Test and quit?                       : 0   [DEFAULT]
Test on one batch at a time?         : 1   [DEFAULT]
Testing frequency                    : 13
```

... a printout of the command-line arguments with which the net was run.

And finally, it starts training, and produces output like this:

```
Saving checkpoints to /storage2/tmp/ConvNet__2011-06-29_22.19.39
=========================
1.1... logprob:  2.277909, 0.879600 (1.563 sec)
1.2... logprob:  2.145043, 0.780400 (1.393 sec)
1.3... logprob:  1.983224, 0.724300 (1.395 sec)
1.4... logprob:  1.913032, 0.702000 (1.395 sec)
1.5... logprob:  1.813073, 0.672400 (1.395 sec)
2.1... logprob:  1.758718, 0.649100 (1.397 sec)
2.2... logprob:  1.735701, 0.637600 (1.397 sec)
2.3... logprob:  1.666571, 0.609900 (1.396 sec)
2.4... logprob:  1.659595, 0.604800 (1.394 sec)
2.5... logprob:  1.605653, 0.584900 (1.395 sec)
3.1... logprob:  1.561900, 0.565300 (1.397 sec)
3.2... logprob:  1.553927, 0.561000 (1.397 sec)
3.3... logprob:  1.497355, 0.538400
======================Test output======================
logprob:  1.538126, 0.553400
-------------------------------------------------------
Layer 'conv1' weights: 1.411148e-02 [6.725948e-05]
Layer 'conv2' weights: 8.830208e-03 [2.333602e-05]
Layer 'conv3' weights: 8.476456e-03 [2.630907e-05]
Layer 'fc10' weights[0]: 1.826295e-03 [1.369660e-04]
-------------------------------------------------------
Saved checkpoint to /storage2/tmp/ConvNet__2011-06-29_22.19.39
======================================================= (1.918 sec)
3.4... logprob:  1.517817, 0.544800 (1.396 sec)
3.5... logprob:  1.481088, 0.526000 (1.399 sec)
4.1... logprob:  1.456526, 0.525100 (1.396 sec)
4.2... logprob:  1.449469, 0.517800 (1.396 sec)
```

... which tells you the epoch and batch numbers as well as the values of all of
the objectives that you're optimizing. The *cost.logreg* objective happens to
return two values -- the average negative log probability of the data under the
model (that's the first number) as well as the classification error rate (the
second number). You can see that the net here is at 55.34% classification error
on the test set. This net will continue training until the epoch number exceeds
that given to the *--epochs* [argument](Options.md) (default 50000).

Every time the net prints a test output, it also saves a checkpoint to the path
printed. The number of checkpoints that it maintains is controlled by the
*--max-filesize* parameter. See [options](Options.md) for more on this parameter.

Included with the test output are measures of the magnitudes of the net's
weights and weight increments (in square brackets). Specifically, the net is
printing the average absolute value of each weight matrix and each weight matrix
increment. This output is useful for spotting learning rates that are too low
(or too high), causing weights to stagnate (or blow up).

If you want to change the learning parameters you specified, you can just kill
the net with Ctrl-C (or kill -9, etc.), change the learning parameters in
[`../example-layers/layer-params-19pct.cfg`](../example-layers/layer-params-19pct.cfg),
and then restart the net like this:

```sh
python convnet.py -f /storage2/tmp/ConvNet__2011-06-29_22.19.39
```

The net will resume from the last checkpoint. If you want to resume from an
earlier checkpoint, pass a specific checkpoint file inside
`/storage2/tmp/ConvNet__2011-06-29_22.19.39` to the `-f` parameter. The
checkpoint files are numbered by their epoch and batch numbers.

### Training on image translations

Most image classification results can be improved by training on slight
translations of the original images. This is an easy way to multiply the amount
of training data available, and hence combat over-fitting.

This code ships with a data provider that's capable of training on translations
of the CIFAR-10, and it isn't hard to adapt it to other datasets. Given the
CIFAR-10, though, here's how you can train on random 24x24 patches of the
original 32x32 images:

```sh
python convnet.py \
    --data-path=/storage2/tiny/cifar-10-batches-py-colmajor/ \
    --save-path=/storage2/tmp \
    --test-range=6 \
    --train-range=1-5 \
    -layer-def=./example-layers/layers-19pct.cfg \
    --layer-params=./example-layers/layer-params-19pct.cfg \
    --data-provider=cifar-cropped \
    --crop-border=4 \
    --test-freq=13
```

This will cause the net to train on random 24x24 patches and test on the center
24x24 patch.

Notice that the only difference between this run line and the one above is that
the data provider has been changed to `cifar-cropped` and we've also added a
`--crop-border=4` argument which indicates the amount of cropping.

After training is done, you can kill the net and re-run it with the
`--test-only=1` and `--multiview-test=1` arguments to compute the test error as
averaged over 10 patches of the original images (4 corner patches, center patch,
and their horizontal reflections). This will produce better results than testing
on the center patch alone.

## Operations on saved nets

### Converting convolutional layers to unshared, locally-connected layers

You may be curious what would happen if you simply untied all of the weights in
a convolutional layer. This is equivalent to converting a
[convolutional](LayerParams.md#convolution-layer) layer to an
[unshared, locally-connected
layer](LayerParams.md#locally-connected-layer-with-unshared-weights). The net
would have many more parameters, as now a different filter would be applied at
each location in the input image. But maybe things will get better?

You can do this like this:

```sh
python convnet.py -f /storage2/tmp/ConvNet__2011-06-29_22.19.39 --conv-to-local=conv3
```

where `conv3` is the name of some convolutional layer in your net. You can
specify multiple layers too, with a comma-delimited list of layer names.

Note that this operation cannot be reversed, except by loading a checkpoint
saved before you did this.

### Decoupling weight matrices between layers

If you defined a layer which [takes its weight matrix from another
layer](LayerParams.md#weight-sharing-between-layers), you may decouple the
weight matrices like this:

```sh
python convnet.py -f /storage2/tmp/ConvNet__2011-06-29_22.19.39 --unshare-weights=conv4
```

where `conv4` is the name of some layer in your net which takes its weight
matrix from another layer. If `conv4` takes
[multiple inputs](LayerParams.md#Layers_with_multiple_inputs) and you want to
decouple a particular weight matrix rather than all of them, you can do this:

```sh
python convnet.py \
    -f /storage2/tmp/ConvNet__2011-06-29_22.19.39 \
    --unshare-weights=conv4[3]
```

This will decouple the *fourth* weight matrix of `conv4`. Indexing starts at 0.

You can also simultaneously decouple weight matrices in multiple layers, by
specifying a comma-delimited list of layer names.

*Note*: once you've decoupled the weight matrices of two layers, they become two
separate, independent entities. This means that they take up twice as much
memory. It also means that the `momW` and `wc` parameters that you specified in
the layer parameter file for the layer that you just unshared now start being
used when updating the newly-created weight matrix.

## Looking inside the net

Now that you know how to train the net, you can [read](ViewingNet.md) about how
to plot the cost function, look at the filters that your net has learned, and
examine the kinds of errors that it makes.
