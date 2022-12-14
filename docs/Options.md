# The command-line arguments that this code takes

## Introduction

If you type

```sh
python convnet.py
```

You should get the following output, briefly describing the command-line arguments that this code expects:

```
convnet.py usage:
    Option                             Description                                          Default
    [--check-grads <0/1>           ] - Check gradients and quit?                            [0]
    [--conserve-mem <0/1>          ] - Conserve GPU memory (slower)?                        [0]
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

You can see that most arguments have default values, so you don't have to provide them.

The angle brackets following the argument names tell you what kind of value each argument expects.

## What they mean

First the optional arguments:

| Argument | Meaning |
|----------|---------|
| `--check-grads` | [Check the gradients](CheckingGradients.md) |
| `--conserve-mem` | Conserve GPU memory by deleting activity and gradient matrices when they're not needed. This will slow down the net but it will allow you to run larger nets.|
| `--conv-to-local` | Convert the specified layers from convolutional to unshared, locally-connected. See [TrainingNet](TrainingNet.md#Convert_convolutional_layers_to_unshared,_locally-connected_laye) for details. |
| `--crop-border` | When using a data provider that crops images (for example if you want to train on translations of the CIFAR-10), this specifies the size of the cropped region in pixels. The `cifar-cropped` data provider does this. |
| `--epochs` | How many epochs to train for. An epoch is one pass through the training data. |
| `-f` | Load checkpoint from given path. All other arguments become optional when this is given. |
| `--gpu` | Set GPU index to run on (default is to grab fastest GPU available). |
| `--logreg-name` | The name of the logistic regression cost objective. To be used in conjunction with the `--crop-border` and `--multiview-test` argument. |
| `--max-filesize` | Maximum amount of disk space occupied by all checkpoints. Set to 0 to only store last checkpoint. |
| `--mini` | Minibatch size. The minibatch size is the number of training cases over which the gradient is averaged to produce a weight update. *For best performance this value should be a multiple of 128.* In particular, this code is in no way designed for on-line learning (i.e. minibatch size of 1). So while a minibatch size of 1 will work, processing 1 image may in general take almost as much time as processing a minibatch of 128 images. |
| `--multiview-test` | When using a data provider that crops images, this indicates that the test error computation should be averaged over several regions of the image rather than just the center region. To be used in conjunction with the `--crop-border` and `--logreg-name` arguments. Note that this will greatly increase the time it takes to compute the test error. So it's best to leave this off until you're done training, at which point you can compute the averaged test error once using this option in conjunction with the `--test-only` option. |
| `--num-gpus` | Ignore this. This code does not support training one model on multiple GPUs. |
| `--test-freq` | The test error computation / checkpoint saving frequency, in units of training batches. Every *this many* training batches,  the net will compute the test error and save a checkpoint.|
| `--test-one` | If multiple testing batches are given, each test output will be computed on only one of the batches. The net will cycle through them in sequence. |
| `--test-only` | Compute the test error and quit. To be used in combination with the `-f` option. |
| `--unshare-weights` | Remove the coupling of weight matrices between layers. See [TrainingNet](TrainingNet.md#decoupling-weight-matrices-between-layers) for details. |
| `--zip-save` | Compress checkpoint files. This makes checkpointing slower and may have almost no effect on the file size. So the default is off. |

Now the mandatory ones:

| Argument | Meaning |
|----------|---------|
| `--data-path` | The path where the net's [data provider](Data.md) can find its data. |
| `--data-provider` | The [data provider](Data.md) to use to parse the data. |
| `--layer-def` | The [layer definition](LayerParams.md#Layer_definition_file) file. |
| `--layer-params` | The [layer parameter](LayerParams.md#Layer_parameter_file) file. |
| `--save-path` | The path to which the net should save checkpoints. |
| `--test-range` | The data [batches](Data.md) that the net should use to compute the test error. |
| `--train-range` | The data [batches](Data.md) that the net should use for training. |
