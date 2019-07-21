"""

Authors: Angel Bueno, Alejandro Diaz.

PICOSS main script for numerical operations.

This script allows the user to perform numerical routines on seismic data streams has been previously processed
and stored/loaded (e.g: miniseed). This script requires the dependencies listed in the file 'requirements.txt'
to be installed within the Python environment you are working.

This file can also be imported as a module and contains the following functions:

    * save_pickle - save the data as a pickle file
    * load_pickle - loads the data from a pickle file
    * load_picking_file - loads the results from a picking file (dictionary with data and thresholds times).
    * plot_signals - Plot an isolated signal and save it.
    * merge_numpy - Gets the numpy signal from an ObsPy stream and merge it.
    * clean_data  - returns the segmented candidates that are above or below a threshold.
    * short_term_energy - returns the short term energy of a signal.
    * energy_per_frame - returns an array containing the energy of the framed signal.
    * plot_signals - Plots a signal, which can be saved or not.

"""

import os

import numpy as np
from six.moves import cPickle
import matplotlib.pyplot as plt


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


def load_picking_file(filename):
    """Function to load the picking file previously processed by our interface"""
    try:
        f = open(filename, 'rb')
        loaded_object = cPickle.load(f)
        f.close()
        return loaded_object
    except (IOError, OSError) as e:
        pass


def plot_signals(signal, label, save=None):
    """Function to plot the a seismic signal as a numpy array.
    Parameters
    ----------
    signal: Numpy Array
         Contains the signals we want to plot
    label: str
         A string containing the label or the signal (or the graph title).
    save: str, optional
        A string containing the picture name we want to save
    -------
    """

    plt.figure(figsize=(10, 8))
    plt.title(label)
    plt.plot(signal)

    if save is not None:
        plt.savefig(save + ".png")

    plt.show()
    plt.close()


def merge_numpy(stream):
    """
    Function that given an ObsPy stream, it merges completely as a numpy array
    Args:
        stream : ObsPy.Stream object.
            The stream we want to merge
    Returns:
    array
        The array as a single numpy array
    """
    data = []
    for k in xrange(len(stream)):
        data.append(stream[k].data)
    return np.asarray(np.hstack(data))


def clean_data(candidate_segmented, fm=100.0, snr_thr=30.0, min_duration=10.0):
    """

    Parameters
    ----------
    candidate_segmented: Numpy Array
        A numpy array containing the segmented candidates.
    fm: float
        The sampling frequency of the candidates.
    snr_thr: float
        The minimum SNR requirement for the candidate
    min_duration: float
        Duration (in seconds) to be considered.

    Returns
    -------
    list
        A list containing just the selected, final candidates.
    """

    new_candidate = copy.copy(candidate_segmented)
    not_wanted = set()

    for k, m in enumerate(candidate_segmented):
        ff = m[0]
        ff = ff - np.mean(ff)
        upper_root = np.sqrt(1 / float(len(ff[0:2000]) * np.sum(np.power(ff[0:2000], 2))))

        noise_root = np.sqrt(1 / float(len(ff[-int(2.0) * int(fm):]) * np.sum(np.power(ff[-int(2.0) * int(fm):], 2))))

        snr = 10 * np.log(upper_root / noise_root)
        samples = len(ff)

        if (len(ff) / float(fm)) <= min_duration:
            not_wanted.add(k)
        elif np.abs(snr) <= snr_thr:
            not_wanted.add(k)
        else:
            pass

    # we need to iterate over new_candidate to avoid mistakes
    return [m for e, m in enumerate(new_candidate) if e not in not_wanted]


def short_term_energy(chunk):
    """Function to compute the short term energy of a signal as the sum of their squared samples.
    Parameters
    ----------
    chunk: Numpy array
        Signal we would like to compute the signal from
    Returns
    -------
    float
        Containing the short term energy of the signal.
    """
    return np.sum((np.abs(chunk) ** 2) / chunk.shape[0])


def energy_per_frame(windows):
    """It computes the energy per-frame for a given umber of frames.

    Parameters
    ----------
    windows: list
        Containing N number of windows from the seismic signal
    Returns
    -------
    Numpy Array
        Numpy matrix, size N x energy, with N the number of windows, energy their associate energy.
    """
    out = []
    for row in windows:
        out.append(short_term_energy(row))
    return np.hstack(np.asarray(out))


def compute_fft(signal, fm):
    """Function to compute the FFT.
    Parameters
    ----------
    signal: Numpy Array.
        The signal we want to compute the fft from.
    fm: float
        the sampling frequency
    Returns
    -------
    Y: Numpy Array
        The normalized fft
    frq: Numpy Array
        The range of frequencies
    """
    n = len(signal)  # length of the signal
    frq = np.arange(n) / (n / fm)  # two sides frequency range
    frq = frq[range(n / 2)]  # one side frequency range
    y = np.fft.fft(signal) / n  # fft computing and normalization
    y = y[range(n / 2)]
    return y, frq






