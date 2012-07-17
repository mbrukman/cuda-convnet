#summary Summary of recent changes to the code.

  * *Jul 17, 2012*
    * Fixed bug in contrast normalization backpropagation code which caused wrong gradients to be computed near image borders. (Thanks Hannes Schulz).
  * *Mar 13, 2012*
    * Added [LayerParams#Local_response_normalization_layer_(across_maps) response-normalization across maps] layer.
    * Started modifying the code to support rectangular (i.e. non-square) images. The convolution code now supports rectangular images, but the remaining code does not yet. So the whole package still requires square images.
  * *Feb 8, 2012*
    * Most layer types now should work well with minibatch size 64 or 32.
    * Fixed --conserve-mem option so it can be combined with -f (i.e. its value can be changed after a net has been saved).
  * *Feb 3, 2012*
    * Convolution with minibatch sizes 32 or 64 should now be about twice as fast (though it's still most optimized for minibatch sizes divisible by 128).
    * Added [Options --conserve-mem] parameter.
  * *Jan 22, 2012*
    * Added some [LayerParams#Color_space_manipulation_layers color space manipulation layers].
  * *Jan 11, 2012*
    * Added [LayerParams#Image_resizing_layer image resizing with bilinear filtering] layer.
  * *Dec 28, 2011*
    * Added ability to [LayerParams#Initializing_weights_from_an_outside_source initialize weights from an outside source]. Thanks to Oriol Vinyals for the suggestion.
    * Layers with zero learning rate no longer waste time computing the gradient.
  * *Dec 22, 2011*
    * Added elementwise max layer, to allow (for example) pooling over scale.
    * Added square, square root neuron activation functions.
    * Added sum-of-squares objective.
  * *Dec 17, 2011*
    * Added Gaussian blur and "bed of nails" subsampling layers.
  * *Dec 9, 2011*
    * All layers with weights (and some others) can now take multiple layers as input.
    * Added the "sum" layer type, which simply performs an elementwise sum of all its input layers.
    * Added support for weight sharing between different layers of the same type. One of the things this allows you to do is to write recurrent networks. Thanks to Ilya Sutskever for the suggestion.
    * Decoupled neuron activation functions from the few layers that supported them. Now you can add a "neuron" layer anywhere in the net, which applies some elementwise function to its input.
    * Most layers now take a neuron=x parameter, which applies some neuron activation function to their outputs.