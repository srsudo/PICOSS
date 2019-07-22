"""

Authors: Angel Bueno, Alejandro Diaz, S. De Angelis and Luciano Zuccarello.

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

"""

import os

import numpy as np
from six.moves import cPickle
import matplotlib.pyplot as plt
from obspy.signal.trigger import classic_sta_lta, recursive_sta_lta, delayed_sta_lta, trigger_onset
from scipy.signal import lfilter, hilbert


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


def compute_ratio(signal, midpoint, fm):
    """
    Function to compute the HF/LF ratio of a given signal, using
    :param signal: the signal we want to compute the HF/LF ratio.
    :param fm: the sampling frequency.
    :return: float . the HF/LF ratio.
    """
    fft, freqs = compute_fft(signal, fm)

    low_band = np.abs(fft[(freqs >= 1) & (freqs <= midpoint)])
    high_band = np.abs(fft[(freqs >= midpoint) & (freqs <= 20)])
    ratio = np.log10(np.mean(np.sum(high_band)) / np.mean(np.sum(low_band)))

    return ratio


def check_masked_array(array):
    """
    Check masked array. Some seismic data is loaded as a masked array, which can lead to numerical problems.
    This functions returns a one-dimensional piecewise linear interpolation from the given discrete masked data points

    Args:
        array : the seismic data array

    Returns:
    Numpy Array
        The numpy array we are computing the data.
    """

    # Check it with the masked arrays on some volcanoes.
    if np.ma.isMaskedArray(array):
        xi = np.arange(len(array))
        mask = np.isfinite(array)
        return np.interp(xi, xi[mask], array[mask])
    else:
        return array


def build_ampa_detector(data, beta, fs, L, lztotal):
    """
    Function that given the impulsiveness (i.e. the enhancement of the impulse response), the sampling frequency
    and the filter duration we want to apply, builds up an optimum enhancement filter for the filterbank detector
    Args:
        beta : float
            The impulsiveness of the enhancement impulse response
        fs : float
            The sampling frequency of the main trace we would like to compute
        l : float
            The filter lenght we will use to compute the response from.
    Returns:
    Numpy array
        The optimum response of the enhancement filter for the proposed impulse response of length l (seconds)
    """

    Ztot = np.zeros((len(L), len(data)))

    for i in xrange(len(L)):
        l = int(L[i] * fs)
        B = np.zeros(2 * l)
        B[0:l] = range(1, l + 1)
        B[l:2 * l] = beta * (np.arange(1, l + 1) - (l + 1))
        Zt = lfilter(B, 1, lztotal, axis=0)
        Zt[Zt < 0] = 0
        Ztot[i, :-l] = np.roll(Zt, -l)[:-l]

    return np.prod(Ztot, 0)[0:]


def multiband_processing(chunked, bandwidth, noise_thr, fc, fs):
    """
    Function that builds up the filter bank to perform multi-band global envelope processing based on pure
    Args:
        chunked : Numpy array
            The numpy array which contains the seismic data to be processed
        bandwidth : float
            The bandwidth we want to use for our group of filters.
        noise_thr : float
            The noise threshold percentile which controls the amount of noise to be reduced
        fc : float
            List containing the set of central frequencies for the
        fs: float
            The sampling frequency required for the data
    Returns:
        Numpy Array
        lztot, or the logarithm of the sum of equalized envelopes
    """
    th = np.arange(0, 32, 1) * (1 / fs)
    f_response = 8 - (np.arange(32) / 4.)
    z = []
    for i in fc:
        frc = (i + i + bandwidth) / 2.0
        h1 = f_response * np.cos(2. * np.pi * frc * th)
        v = lfilter(h1, 1, chunked)  # filter and envelop detector
        e = np.abs(hilbert(v))
        # from the envelop, noise reduction
        tr = np.percentile(e, noise_thr)
        z.append((e / tr) * (e > tr) + (e <= tr))

    z = np.sum(np.hstack(z), axis=1)
    # For numerical reason, we compute the logarithm from the total CF.
    return np.log10(z) - np.min(np.log10(z)) + 1e-32


def compute_sta_lta(data, fm, trigger_type, nlta=10.0, nsta=5.0, trig_on=1.2, trig_off=0.5):
    """
    Function that handles the building of STA/LTA event picking: classic, recursive and delayed. It follows Obspy
    implementation of these algorithms and can be interfaced with the main GUI to plot the results, or with the
    CLI to other analysis routines. A detailed comparison of STA/LTA techniques algorithms are included in:

    Withers, M., Aster, R., Young, C., Beiriger, J., Harris, M., Moore, S., and Trujillo, J. (1998),
    A comparison of select trigger algorithms for automated global seismic phase and event detection,
    Bulletin of the Seismological Society of America, 88 (1), 95-106.
    http://www.bssaonline.org/content/88/1/95.abstract

    Args:
        data : Numpy Array
            The seismic data we want to apply our STA/LTA routine
        fm : float
            The sampling frequency of the main trace
        trigger_type : str
            A string identifiying which trigger type we want (Recursive, Delayed, Classic)
        nlta : float
            Length of the Long Time Average Window (LTA)
        nsta : float
            Length of the Short Time Average Window (STA)
        trig_on : float
            Value of the CF to consider as an activation trigger
        trig_off : float
            Value of the CF to consider as a de-activation trigger
    Returns:
        cft: Numpy Array
            The characteristic function result of the
        on_of: Tuple
            A data tuple containing the on/ofs times of the even picking
    """

    if np.isnan(data).any():
        to_process = filtered.copy()
        data = merge_numpy(to_process)

    try:

        if trigger_type == "Recursive":
            cft = recursive_sta_lta(data, int(nsta * fm), int(nlta * fm))
        elif trigger_type == "Delayed":
            cft = delayed_sta_lta(data, int(nsta * fm), int(nlta * fm))
        else:
            cft = classic_sta_lta(data, int(nsta * fm), int(nlta * fm))

        on_of = trigger_onset(cft, trig_on, trig_off)

        return cft, on_of

    except ArithmeticError:
        print "Problem whilst computing the trigger"


def compute_ampa(data, fm, window, bandwidth, f_init, f_end, overlap, noise_threshold, u_value, beta, filters):

    """
    Compute AMPA algorithm, an automatic P-Phase picking algorithm based on Adaptive Multi-band processing. Two stages
    are identified within this algorithm: 1) the adaptative multiband processing and 2) the enhancement filter stage.
    On the first stage, the multi-band processing aims to minimize the effect of background noise by computing a global
    envelop from each frequency band. The second stage, aims to find an optimum impulse response of the enhancement
    filter for a set of different duration impulse responses. For a detailed description, please refer to:

    I. Alvarez, L. Garcia, S. Mota, G. Cortes, C. Benitez and A. De la Torre,
    "An Automatic P-Phase Picking Algorithm Based on Adaptive Multiband Processing,"
    in IEEE Geoscience and Remote Sensing Letters, vol. 10, no. 6, pp. 1488-1492, Nov. 2013.doi: 10.1109/LGRS.2013.2260720

    Notice that this implementation follows the same modular approach as the proposed in the manuscript.

    Args:
        data : Numpy Array
            A numpy array containing the seismic signal we would like to process the data
        fm : float
            The sampling frequency of the seismic signal
        window : float
            The window of analysis in windows.
        bandwidth : float
            The bandwidth of the filters
        f_init : float
            The initial frequency of the filterbank.
        f_end : float
            The end frequency of the filterbank.
        overlap : float
            The total amount of overlap (percentage) to
        noise_threshold : float
            The percentile value over we would like to reduce the noise
        u_value: float
            U is related with the level of the global envelope that is ignored
        beta: float
            The impulsiveness of the proposed impulse response
        filters: list
            A list of filters for our filterbank central frequencies
    Returns:
        on : Numpy Array
            A set of values with the on activation values
    """

    if filters is None:
        # in case no filter were added by the user, use the default ones
        filters = [30., 20., 10., 5., 2.5]


    ######## Uncomment for test
    fs = fm
    threshold = None
    filters = [30., 20., 10., 5., 2.5]
    beta = 3. #beta
    noise_thr = 90
    bandwidth = 3.
    overlap = 1.
    f_init = 2.
    f_end = 12.
    u_value = 12.
    peak_window = 1.
    ###########

    window = 50.0
    duration = data.shape[0] / float(fm)
    delta = bandwidth - overlap
    fc = np.arange(f_init, f_end + delta, delta)  # set of central frequencies.
    on = []
    c = 0

    for x in xrange(0, int(duration), int(window)):
        # we need to chunk the data, index the trace and get the
        chunked = data[int(x*fm):int((x+window)*fm)].reshape(-1, 1)
        lztot = multiband_processing(chunked, bandwidth, noise_thr, fc, fs)
        cf = build_ampa_detector(chunked, beta, fs, filters, lztot)
        peac = np.where(cf == np.amax(cf))[0][0]  # the maximum peak
        on.append(x*fm+peac)
        del lztot, peac, cf, chunked
        c = c+1
        if c == 5:
            break

    on = np.vstack(on)
    del fc, delta
    return on


def run_classification_fi(data, f):
    pass