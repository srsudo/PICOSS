import os

import numpy as np
from six.moves import cPickle


def save_pickle(destination_folder, filename, data):
    """
    Function that given a destination folder, a file and a data structure, saves it on a folder accordingly.
    Args:
        destination_folder : str
            The destination folder where we want to save
        file : str
            The file we would like to save
        data : Array
            The data structure we would like to save
    """
    f = open(os.path.join(destination_folder, filename), 'wb')
    cPickle.dump(data, f, protocol=cPickle.HIGHEST_PROTOCOL)
    f.close()


def load_pickle(folder, filename):
    """
    Function that given a reading folder, and a filename, load the data structure we would like to work with.
    Args:
        folder : str
            The folder we would like to read from
        filename : str
            The filename we would like to read from
    Returns:
    array
        The loaded object we want to work with.
    """
    try:
        f = open(os.path.join(folder, filename), 'rb')
        loaded_object = cPickle.load(f)
        f.close()
        return loaded_object
    except (IOError, OSError) as e:
        pass


def plot_signal():
    raise NotImplementedError


def merge_numpy(stream):
    """
    Function that given an Obspy stream, it merges completely as a numpy array
    Args:
        stream : Obspy.Stream object.
            The stream to merge
    Returns:
    array
        The array as a single numpy array
    """


    data = []
    for k in xrange(len(stream)):
        data.append(stream[k].data)
    return np.asarray(np.hstack(data))

