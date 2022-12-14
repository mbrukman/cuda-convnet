# How to verify that the gradients computed by the net are correct

*Note: the only reason to read this section is if you suspect a bug in the code.*

## Testing the gradients

This code is capable of using a finite-difference calculation to numerically
test the gradients that it computes for training. It can only do this on small
models, because numerically computing a gradient for each weight is highly
computationally-intensive.

But here's how to do it. You should read the [layer params](LayerParams.md) and
[training net](TrainingNet.md) sections first so you're familiar with how to run
the net.

*Note also that in order for the numerical gradient testing computation to
produce accurate results, you will need to use bigger weight initializations
than you normally would (that's the `initW` parameter in layers that have
weights).*

Once you've checked out the code, you can find some dummy architecture
definition files in the [`../example-layers`](../example-layers) subdirectory.
You can verify the gradients computed for that dummy architecture with this
line:

```sh
python convnet.py \
    --layer-def=./example-layers/layers.gc.cfg \
    --layer-params=./example-layers/layer-params.gc.cfg \
    --data-provider=dummy-cn-192 \
    --check-grads=1
```

Notice that we're using a dummy data provider to produce 192-dimensional input,
which is interpreted by the net as 8x8 3-channel images (see the `conv32` layer
in layer definition file).

You'll see output that, in my case, looks like this:

```
Initialized data layer 'data', producing 192 outputs
Initialized data layer 'labels', producing 1 outputs
Initialized convolutional layer 'conv32', producing 6x6 16-channel output
Initialized convolutional layer 'conv32-2', producing 3x3 16-channel output
Initialized fully-connected layer 'fc10', producing 10 outputs
Initialized softmax layer 'probs', producing 10 outputs
Initialized logistic regression cost 'logprob'
=========================
Importing _ConvNet C++ module
=========================
Training ConvNet
Check gradients and quit?   : 1
Compress checkpoints?       : 0     [DEFAULT]
Data batch range: testing   : 0-0
Data batch range: training  : 0-0
Data path                   :
Data provider               : dummy-cn-192
GPU override                :       [DEFAULT]
Layer definition file       : ./layers.gc.cfg
Layer parameter file        : ./layer-params.gc.cfg
Load file                   :       [DEFAULT]
Maximum save file size (MB) : 0     [DEFAULT]
Minibatch size              : 128   [DEFAULT]
Number of GPUs              : 1     [DEFAULT]
Number of epochs            : 50000 [DEFAULT]
Save path                   :
Test and quit?              : 0     [DEFAULT]
Test on one batch at a time?: 1     [DEFAULT]
Testing frequency           : 50    [DEFAULT]
=========================
Running on CUDA device(s) -2
Current time: Thu Jun 30 20:38:02 2011
Saving checkpoints to ConvNet__2011-06-30_20.38.02
=========================
2.1...------------------------
ALL 7 TESTS PASSED
```

The model verifies the gradients of each of the weight matrices in the net. In
this case there are 7 of them. Had any of the gradient tests failed, the model
would have printed out the relative error between the results of the analytic
computation and the numerical one. The relative error between two vectors is

$$ \frac{\lVert x_1 - x_2 \rVert}
        {\lVert x_1       \rVert}
$$

In the file [`util.cuh`](../include/util.cuh), there are these two lines:

```c
#define GC_SUPPRESS_PASSES     true
#define GC_REL_ERR_THRESH      0.02
```

The first one controls whether anything should be printed for gradients that
pass. The second defines what a pass is. You can see that at present, any
relative error smaller than 0.02 (2%) is considered a pass.

But please note that in general, numerical gradient testing is a bit of a black
art. Nonlinearities in the network, especially in deep networks, make it
difficult to accurately estimate the gradient with finite differences. A
relative error greater than 2% does not _necessarily_ mean that the analytic
gradient was computed incorrectly. I heuristically and arbitrarily chose a
relative error of 2% as the threshold between "pass" and "fail". Anything around
10% almost certainly means the gradient was computed correctly.

Each layer type in [`layer.cu`](../src/layer.cu) defines a `checkGradients`
method, in which it specifies the _epsilon_ that should be used in the equation

$$ f'(x) = \frac{f(x + \varepsilon) - f(x)}{\varepsilon} $$

which is used to numerically compute the gradients. My experience has been that
if your gradients are computed correctly, it's possible to find a value of
_epsilon_ to make the numerical computation match the analytic one to a high
degree of accuracy. If your gradients are computed incorrectly, this is
impossible.
