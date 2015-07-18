__author__ = 'nparslow'

# adapted from
# https://github.com/lisa-lab/pylearn2/blob/master/pylearn2/scripts/tutorials/grbm_smd/make_dataset.py


# This script creates a preprocessed version of a dataset using pylearn2.
# It's not necessary to save preprocessed versions of your dataset to
# disk but this is an instructive example, because later we can show
# how to load your custom dataset in a yaml file.
#
# This is also a common use case because often you will want to preprocess
# your data once and then train several models on the preprocessed data.

import os.path
import pylearn2
import codecs

import gensim

# We'll need the serial module to save the dataset
from pylearn2.utils import serial


categoriesToKeep = {'v', 'nc', 'adj', 'adv'}
ends_categoriesToKeep = tuple(["_" + y for y in categoriesToKeep])
model = gensim.models.Word2Vec.load('mymodel.word2vec')

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in codecs.open(os.path.join(self.dirname, fname), encoding="utf-8", mode="r"):
                # todo clean up here
                tokens = line.split()
                #print [x for x in tokens if x.endswith(ends_categoriesToKeep)]
                yield [x for x in tokens if x.endswith(ends_categoriesToKeep)]
                #yield line.split()

# We'll need the preprocessing module to preprocess the dataset
from pylearn2.datasets import preprocessing

if __name__ == "__main__":
    # Our raw training set is 32x32 color images
    train = cifar10.CIFAR10(which_set="train")

    # We'd like to do several operations on them, so we'll set up a pipeline to
    # do so.
    pipeline = preprocessing.Pipeline()

    # First we want to pull out small patches of the images, since it's easier
    # to train an RBM on these
    pipeline.items.append(
        preprocessing.ExtractPatches(patch_shape=(8, 8), num_patches=150000)
    )

    # Next we contrast normalize the patches. The default arguments use the
    # same "regularization" parameters as those used in Adam Coates, Honglak
    # Lee, and Andrew Ng's paper "An Analysis of Single-Layer Networks in
    # Unsupervised Feature Learning"
    pipeline.items.append(preprocessing.GlobalContrastNormalization(
        sqrt_bias=10., use_std=True))

    # Finally we whiten the data using ZCA. Again, the default parameters to
    # ZCA are set to the same values as those used in the previously mentioned
    # paper.
    pipeline.items.append(preprocessing.ZCA())

    # Here we apply the preprocessing pipeline to the dataset. The can_fit
    # argument indicates that data-driven preprocessing steps (such as the ZCA
    # step in this example) are allowed to fit themselves to this dataset.
    # Later we might want to run the same pipeline on the test set with the
    # can_fit flag set to False, in order to make sure that the same whitening
    # matrix was used on both datasets.
    train.apply_preprocessor(preprocessor=pipeline, can_fit=True)

    # Finally we save the dataset to the filesystem. We instruct the dataset to
    # store its design matrix as a numpy file because this uses less memory
    # when re-loading (Pickle files, in general, use double their actual size
    # in the process of being re-loaded into a running process).
    # The dataset object itself is stored as a pickle file.
    path = pylearn2.__path__[0]
    train_example_path = os.path.join(path, 'scripts', 'tutorials', 'grbm_smd')
    train.use_design_loc(os.path.join(train_example_path,
                                      'cifar10_preprocessed_train_design.npy'))

    train_pkl_path = os.path.join(train_example_path,
                                  'cifar10_preprocessed_train.pkl')
