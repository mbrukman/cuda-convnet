# Neuron types

The types of neurons (hidden unit nonlinearities) supported by the net.

Most of the [layer types](LayerParams.md) take a `neuron=x` parameter, which
defines the output nonlinearity of neurons in the layer.

These are the supported neuron types:

| Parameter            | Name                     | Function                          |
|----------------------|--------------------------|-----------------------------------|
| `neuron=logistic`    | logistic                 | $f(x) = 1/(1 + e^{-x})$           |
|`neuron=tanh[a,b]`    | hyperbolic tangent       | $f(x) = a \cdot \tanh(b \cdot x)$ |
| `neuron=relu`        | rectified linear         | $f(x) = \max(0, x)$               |
| `neuron=brelu[a]`    | bounded rectified linear | $f(x) = \min(a, \max(0, x))$      |
| `neuron=softrelu`    | soft rectified linear    | $f(x) = \log(1 + e^x)$            |
| `neuron=abs`         | absolute value           | $f(x) = \lvert x \rvert$          |
| `neuron=square`      | square                   | $f(x) = x^2$                      |
| `neuron=sqrt`        | square root              | $f(x) = \sqrt{x}$                 |
| `neuron=linear[a,b]` | linear                   | $f(x) = ax + b$                   |

$x$, $a$, and $b$ above are all scalars.

Adding new types of neurons is easy. See [`neuron.cuh`](../include/neuron.cuh)
for reference.
