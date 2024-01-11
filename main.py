# This algorithm is designed to compress grayscale images in a lossy manner.
# We aim to replace homogeneous areas with
# single-color squares for simpler representation. This seems to reduce the jpg filesize a lot,
# though unsure about the mechanism behind this since JPG is DCT-based...
# Oddly enough the filesizes don't seem to always reduce when using PNG images?


import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':18})

img = np.array([[2,2,2,2,2,1,1,1],
               [2,0,2,0,2,2,2,2],
               [2,2,2,2,2,2,2,2],
               [2,2,1,3,1,1,1,3],
               [2,2,1,1,1,1,1,1],
               [2,2,1,1,1,3,1,1],
               [2,2,2,2,2,2,2,2],
               [2,2,2,2,2,2,2,2]])

# IMAGE DIMENSIONS NEED TO BE POWERS OF 2!
#imname = 'Tree'
#imname = 'Icebath'
imname = 'Cat'

img = cv2.imread(imname + '.jpg')
# Convert to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def compress_img(img, treshold, depthmap, depth):
    block_size = len(img)
    img_compressed = np.ndarray(np.shape(img))
    # Get the mean absolute deviation
    mad_curr = np.mean(np.absolute(img - np.mean(img)))
    # If mad is small enough (image is homogeneous), replace the batch with its mean value
    if mad_curr <= treshold:
        img_compressed[:,:] = np.mean(img)
        depthmap[:,:] = depth
    # If image is not homogeneous, split the image batch into four pieces and
    # run the algorith recursively on them
    else:
        h = int(block_size/2)
        img_compressed[0:h, 0:h], depthmap[0:h, 0:h] = compress_img(img[0:h, 0:h], treshold, depthmap[0:h,0:h], depth+1)
        img_compressed[0:h, h:block_size], depthmap[0:h, h:block_size] = compress_img(img[0:h, h:block_size], treshold, depthmap[0:h, h:block_size], depth+1)
        img_compressed[h:block_size, 0:h], depthmap[h:block_size, 0:h] = compress_img(img[h:block_size, 0:h], treshold, depthmap[h:block_size, 0:h], depth+1)
        img_compressed[h:block_size, h:block_size], depthmap[h:block_size, h:block_size] = compress_img(img[h:block_size, h:block_size], treshold, depthmap[h:block_size, h:block_size], depth+1)
    return img_compressed, depthmap


# This adjusts the amount of compression
treshold = 12
# This will show the depth reached in the recursive algorithm, for each pixel, which
# is also related to the size of the constant-valued block it is in
depthmap = np.zeros(np.shape(img))

img_compressed, depthmap = compress_img(img, treshold, depthmap, depth=0)

# Save the compressed image
plt.imsave(imname + '_compressed.jpg', img_compressed, cmap='gray')

# Read the original and compressed file sizes to compare
filesize_orig = os.path.getsize(imname + '.jpg')
filesize_comp = os.path.getsize(imname + '_compressed.jpg')
compd_relsize = 100*(filesize_comp/filesize_orig)

plt.figure()
plt.subplot(1, 3, 1)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.subplot(1,3,2)
plt.title("Compressed to " + str(round(compd_relsize)) + "%")
plt.imshow(img_compressed, cmap='gray')
plt.subplot(1,3,3)
plt.title('Blocks')
plt.imshow(depthmap)
plt.show()







