# cuda-convnet

High-performance C++/CUDA implementation of abstract convolutional neural networks.

This is an export of the
[**cuda-convnet**](http://code.google.com/p/cuda-convnet/) project from Google
Code, with some cleanups for readability.

It contains the implementation of the [AlexNet][alexnet] Convolutional Neural
Network model for image recognition that was state-of-the-art at the time of its
release.

## Contributing

This is an export of the project listed above, with some cleanups for better
readability, but I do not plan to develop it further, and as such, I am not
looking to accept any contributions at this time.

Rather than getting this project to work as-is (which would mean having to
migrate it to newer versions of Python, CUDA, etc.), and resolving various
compatibility issues with decade-old software, I am reimplementing this and
other ML papers in [another project][reimplementing] if you would like to follow
along.

If you would like to continue the development of this project, please feel free
to fork it, or contribute to another existing fork.

## License

BSD-2-Clause license; see [`LICENSE`](LICENSE) for details.

[alexnet]: https://en.wikipedia.org/wiki/AlexNet
[reimplementing]: https://github.com/mbrukman/reimplementing-ml-papers
