# How to compile the code

**Note:** A Fermi-generation GPU (GTX 4xx, GTX 5xx, or Tesla equivalent) is
required to run this code. Older GPUs won't work. Newer (Kepler) GPUs also will
work, but as the GTX 680 is a terrible, terrible GPU for non-gaming purposes, I
would not recommend that you use it. (It will be slow).

## On Linux

### Required libraries

Here's what I hope to be a complete list of prerequisite libraries. Please
[email me](mailto:akrizhevsky@gmail.com) if I'm wrong.

| Library | Ubuntu package name | Fedora package name |
|---------|---------------------|---------------------|
| Python development libraries/headers | python-dev | python-devel |
| Numpy | python-numpy | numpy |
| Python libmagic bindings | python-magic | python-magic |
| Matplotlib | python-matplotlib | python-matplotlib |
| ATLAS development libraries/headers | libatlas-base-dev | atlas-devel |

Implicit in this list are all the packages on which the above packages depend
(for example, python-magic depends on libmagic, etc.).

And of course you also need to install the CUDA toolkit and CUDA SDK (versions
4.0, 4.1, and 4.2 will work).

Ideally you should be running a 64-bit Linux system, as I do not know whether
this code works on 32-bit systems.

### Compiling

In the main directory, you'll find the [`build.sh`](../build.sh) file. Fill in
the environment variables in that file (the included defaults are the proper
values on _my_ system, but almost certainly not on yours).

Then, type

```sh
sh build.sh
```

If all goes well, in a few minutes the compilation will finish successfully.
[Email me](mailto:akrizhevsky@gmail.com) in case of trouble.

## On Windows

It's possible, but perhaps not easy, to compile and use this code on Windows. I
have no means of testing it myself, but Oriol Vinyals has kindly provided [this
Visual Studio 2010
project](http://code.google.com/p/cuda-convnet/downloads/detail?name=cuda-convnet-vs-proj.zip)
with which he was able to compile and run the code.

He notes that you will have to

* Point Visual Studio to the location of your MKL install.
* Compile with the `USE_MKL` preprocessor macro defined.
* Replace the dependency on pthreads with [pthreads-win32](https://sourceware.org/pthreads-win32/).

Good luck.
