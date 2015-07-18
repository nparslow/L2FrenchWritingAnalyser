__author__ = 'nparslow'

import theanets
import skdata.mnist
import numpy as np
import matplotlib.pyplot as plt


exp = theanets.Experiment(
    theanets.Classifier,
    layers = (784, 100, 10)
)

def load_mnist():
    mnist = skdata.mnist.dataset.MNIST()
    mnist.meta # trigger download if needed.

    def arr(n, dtype):
        # convert an array to the proper shape and dtype
        arr = mnist.arrays[n]
        return arr.reshape((len(arr), -1)).astype(dtype)

    train_images = arr('train_images', 'f') / 255. # rescale pixel intensity to be in 0-1 instead of 0-255
    train_labels = arr('train_labels', np.uint8)
    test_images = arr('test_images', 'f') / 255.
    test_labels = arr('test_labels', np.uint8)
    # most data will need to be cast to floatX in Theano
    return ((train_images[:10000], train_labels[:10000,0]),
            (train_images[10000:20000], train_labels[10000:20000,0]),
            (test_images, test_labels[:, 0]))

train, valid, test = load_mnist()

exp.train(train,
          valid,
          optimize='nag', # default RmsProp, nag = Nesterov's Accelerated Gradient (sgd with momentum)
          learning_rate=1e-3,
          momentum=0.9)

img = np.zeros((28*10, 28*10), dtype='f')
for i, pix in enumerate(exp.network.find(1,0).get_value().T):
    r, c = divmod(i, 10)
    img[r * 28: (r+1)*28, c * 28: (c+1)*28] = pix.reshape((28,28))
plt.imshow(img, cmap=plt.cm.gray)
plt.show()

#predicted_class = exp.network.predict(new_digit)