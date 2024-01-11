This algorithm is designed to compress grayscale images in a lossy manner. We aim to replace homogeneous areas with single-color squares for simpler representation. This seems to reduce the jpg filesize a lot, though unsure about the mechanism behind this since JPG is DCT-based...
Oddly enough the filesizes don't seem to always reduce when saving in PNG format?

Some example results

![image](https://github.com/JoelEnwald/SimpleImageCompressor/assets/6623412/ea258da6-241d-48b8-a668-d4179d57f44b)

The percentages mean that the filesize of the compressed image has dropped to that portion of the original.
