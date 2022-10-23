# Neuron types

The types of neurons (hidden unit nonlinearities) supported by the net.

Most of the [layer types](LayerParams.md) take a `neuron=x` parameter, which
defines the output nonlinearity of neurons in the layer.

These are the supported neuron types:

| Parameter | Name | Function |
|-----------|------|----------|
| `neuron=logistic` | logistic | ![](images/logistic.gif) |
|`neuron=tanh[a,b]` | hyperbolic tangent | ![](images/tanh.gif) |
| `neuron=relu` | rectified linear | ![](images/relu.gif) |
| `neuron=brelu[a]` | bounded rectified linear | ![](images/brelu.gif) |
| `neuron=softrelu` | soft rectified linear | ![](images/softrelu.gif) |
| `neuron=abs` | absolute value | ![](images/abs.gif) |
| `neuron=square` | square | ![](images/square.gif) |
| `neuron=sqrt` | square root | ![](images/sqrt.gif) |
| `neuron=linear[a,b]` | linear | ![](images/linear.gif) |

_x_, _a_, and _b_ above are all scalars.

Adding new types of neurons is easy. See [`neuron.cuh`](../include/neuron.cuh)
for reference.
