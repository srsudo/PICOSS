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
import obspy
from obspy.signal.trigger import classic_sta_lta, recursive_sta_lta, delayed_sta_lta, trigger_onset
from scipy.signal import lfilter, hilbert
from scipy import io
from scipy.stats import entropy as sci_entropy
import gc
from segment_axis import segment_axis

def write_tofile(file_path, text):
    """
    Function that writes information on a plain file.
    Args:
        file_path : Str
            The file path where we would like to store the final file
        text : Str
            The text we want to write in.
    """
    with open(file_path, 'a+') as outfile:
        outfile.write(str(text) + "\n")


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


def load_processed_file(filename):
    """Function to load the picking file previously processed by our interface
    Returns:
        loaded_object: A list with the processed picking file we are using.
    """
    try:
        f = open(filename, 'rb')
        loaded_object = cPickle.load(f)
        f.close()
        return loaded_object
    except (IOError, OSError) as e:
        pass


def load_segmentation(filestring):
    """
    Function that checks the extension of a segmentation file and load the segmentation times.
    Args:

        filestring : str
            This filestring is the string of the file we want to check the extension from.
    Returns:
    Numpy Array
        A numpy array containing the segmentation times.
    """
    extension = filestring.split(".")[-1]
    seg_times = None
    try:
        if extension == "npy":
            seg_times = np.load(filestring)
        elif extension == "p":
            seg_times = load_processed_file(filestring)
        else:
            """Serialize an object into matlab format."""
            seg_times = io.loadmat(filestring)
    except:
        seg_times = None

    gc.collect()
    # example of loaded data ['206.16', '214.0', 'U', '8652.82', '7.84', '1', '']
    return seg_times


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


def process_trace(filename, bandpass=None):
    """
    This function reads a stream, detrend and filter and merge the data into a single numpy trace
    Args:
        filename : str
            The filename of the
        bandpass : list
            A list containing the bandpass filter, if required.
    Returns:
    Trace :Numpy array
        The numpy array containing the loaded seismic data.
    sampling_frequency : Float
        The sampling frequency of the loaded seismic data.
    """

    stream = obspy.read(filename).detrend()
    if bandpass is not None:
        filtered = stream.filter("bandpass", freqmin=bandpass[0], freqmax=bandpass[1])
        trace = filtered.merge(method=0)
    else:
        trace = stream.merge(method=0)

    sampling_frequency = trace[0].stats.sampling_rate

    return trace[0], sampling_frequency


def process_segmentation_table(filename_seg):
    """
    Function that reads the saved file of a segmentation table, and performs a single
    Args:
        filename_seg : str
            The filename we would like to read the segmentation table from.
    Returns:
    List
        The segmentation on/off of the file.
    """
    seg_times = load_segmentation(filename_seg)
    return np.asarray([l[:2] for l in seg_times[2:]], dtype=float)


def extract_signals(data, fs, segmentation_times):
    """
    Signal that given the set of segmentation times, extract the signal from the raw trace.
    Args:
        data : Numpy
            The input seismic data containing both, start and end times of the seismic data.
        fs : float
            The sampling frequency.
        segmentation_times : list
            A list containing the segmentation of the file

    Returns:
    List
        A list containing the extracted signals.
    """
    signals = []
    durations = []
    for m in segmentation_times:
        segmented = data[int(m[0] * fs): int(m[1] * fs)]
        signals.append(segmented)
        durations.append(segmented.shape[0]/float(fs))

    return signals, durations


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
    frq = np.arange(n) / float((n / fm))  # two sides frequency range
    frq = frq[range(n / 2)]  # one side frequency range
    y = np.fft.fft(signal) / float(n)  # fft computing and normalization
    y = y[range(n / 2)]
    return y, frq


def compute_ratio(signal, midpoint, fm):
    """
    Function to compute the HF/LF ratio of a given signal, using the FFT criteria
    :param signal: the signal we want to compute the HF/LF ratio.
    :param fm: the sampling frequency.
    :return: float . the HF/LF ratio.
    """
    fft, freqs = compute_fft(signal, fm)
    low_band = np.abs(fft[(freqs >= 1) & (freqs <= midpoint)])
    high_band = np.abs(fft[(freqs >= midpoint) & (freqs <= 20)])
    return np.log10(np.mean(np.sum(high_band)) / np.mean(np.sum(low_band)))


def evaluate_candidates(signal, slider_md, fm):
    """
    Function to evaluate the HF/LF ratios of given signals, using the compute_ratio function
    :param signal: the signal we want to compute the HF/LF ratio.
    :param fm: the sampling frequency.
    :return: float . the HF/LF ratio.
    """
    ratios = []
    for m in signal:
        ratios.append(compute_ratio(m, slider_md, fm))
    return ratios


def evaluate_ratios(ratios, durations, thr_dur = 25.0, mu_low=-0.5, mu_high=0.5, mu_rock=0.2, mixed=None):
    """
    This functions evaluates the frequency ratios as described in:

    Bueno, A., Diaz-Moreno, A., De Angelis, S., Benitez, C., Ibanez, J.M. (2019).
    Recursive Entropy Method of Segmentation for Seismic Signals. 90 (4): 1670-1677.
    doi: https://doi.org/10.1785/0220180317

    The output are the labels of the events, and can be used for building up seismic datasets.
    Args:
        ratios : Numpy Array
            The numpy array that contains the computed ratios from the segmented candidates
        durations : Numpy Array
            The numpy array that contains the computed durations from the segmented candidates
        mu_low : float
            The threshold used for the low frequency events
        mu_high : float
            The threshold used for the high frequency events
        mu_rock : float
            The threshold used for the rockfall vs tre frequency events

        mixed : List
            A list of events that can be used

    Returns:
    Numpy array:
        A numpy array containing the assigned labels
    """
    lbl = []
    # concatenate both

    mu_hybridhigh = mu_high  # by default
    mu_hybridlow = mu_low

    if mixed is not None:
        mu_hybridlow  = mixed[0]
        mu_hybridhigh = mixed[1]

    for m in zip(ratios, durations):
        if m[1] < thr_dur:

            if m[0] <= mu_low:
                lbl.append('lf')

            elif m[0] >= mu_low:
                lbl.append('hf')

            elif mu_hybridlow < m[0] < mu_hybridhigh:
                lbl.append('mx')

        elif m[1] > thr_dur and m[0] < mu_rock:
            lbl.append('tre')
        else:
            lbl.append('rock')

    return np.asarray(lbl)


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
        data = merge_numpy(data)
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


def run_segmentation(stream, data, on_of, delay_in, durations_window, epsilon=2.5, plot=False, cut="original"):

    """ Function that executes the main segmentation. Additional pre-processing steps might be required. Please, refer
    to the main manuscript and do cite if you are suing this algorithm:

    Recursive Entropy Method of Segmentation for Seismic Signals. A. Bueno1, A. Diaz-Moreno, S. De Angelis,
    C. Benitez and J.M.Ibanez. Seismological Research Letters (SRL).

    It is assumed that the seismic data streams has been previously processed and stored in an correct format
    (e.g: miniseed). In practice, if the data can be stored in NumPy format, it can be processed in Python.

    or github.com/srsudo/remos for additional examples.

    Parameters
    ----------
    stream: Stream Obspy
        The original Stream Obspy object
    data: Numpy Array
        The PROCESSED data from the STA/LTA method
    on_of:
        The numpy matrix, size nsamples x 2, containing the timing
    delay_in: float
        The offset defined to cut from the estimated number of windows
    durations_window: list
        An array containing [W_s, W_d] the window search duration and the minimum window.
    epsilon: float, optional
        The threshold value for the entropy
    plot: bool, optional
        True if we want to plot eacf ot the segmented signals. Be vareful for long streams (>25 min)
    cut:string, optional
        "original" to cut from the main trace, or "processed" to cut from the STA/LTA filtered trace.
    Returns
    X: list
        A list containing the [signal, FI_ratio, start, end]
    -------
    """

    # we make a copy in memory of the original array
    array_original = stream[0].copy()

    # mean removal, high_pass filtering of earth noise background
    array_original = array_original.detrend(type='demean')
    array_original.data = obspy.signal.filter.highpass(array_original.data, 0.5, df=array_original.stats.sampling_rate)

    fm = float(array_original.stats.sampling_rate)
    X = []

    window_size = durations_window[0]
    search_window = durations_window[1]

    data = data - np.mean(data)
    processed_data = data.copy()

    # use the percentile to reduce background
    umbral = np.percentile(data, 80)
    data = (data / float(umbral) * (data > umbral)) + (0 * (data <= umbral))

    for m, k in enumerate(on_of):

        # c = c + 1
        start = int(k[0])
        end = int(k[1])

        x_0 = int(start - delay_in * fm)
        x_1 = np.abs(x_0 - int(start - delay_in * fm + end + search_window * fm))

        selected_candidate = np.asarray(data[x_0:x_1])
        ventanas = segment_axis(selected_candidate.flatten(), int(window_size * fm), overlap=0)
        energy_ventanas = energy_per_frame(ventanas)
        total_energy = np.sum(energy_ventanas)
        loq = energy_ventanas / float(total_energy)

        if sci_entropy(loq) < epsilon:
            cut_me = int(np.argmin(loq) * window_size * fm + delay_in * fm)
            potential_candidate = array_original[x_0:cut_me + x_0]
            duration_candidate = potential_candidate.shape[0] / float(fm)

            if duration_candidate < 5.0:
                # By doing this, we erase those windows with small durations
                pass

            else:

                potential_candidate = potential_candidate - np.mean(potential_candidate)
                ventanas_ref = segment_axis(potential_candidate.flatten(), int(5.0 * fm), overlap=0)

                try:
                    dsai = int((ventanas_ref.shape[0] / 2.0))
                except:
                    dsai = 0

                try:
                    down_windows = energy_per_frame(ventanas_ref[0:dsai])
                    upper_windows = energy_per_frame(ventanas_ref[dsai:dsai + dsai])
                    ratio = np.round(np.sum(np.asarray(upper_windows)) / np.sum(np.asarray(down_windows)), 2)
                except:
                    ratio = np.inf
                    pass

                if ratio < 0.15:
                    # In this case, long-segmentation, re-cut.
                    try:
                        ind = np.sort(np.argpartition(upper_windows, 2)[:2])[0]
                    except:
                        # print "on exception"
                        ind = upper_windows.shape[0]

                    min_duration = (down_windows.shape[0] + ind) * 5.0 * fm
                    cut_me = int(min_duration)

            if cut == "original":
                selected_candidate = array_original.data[x_0:cut_me + x_0]
                X.append([selected_candidate, ratio, x_0, cut_me + x_0])
            else:
                selected_candidate = processed_data[x_0:cut_me + x_0]
                X.append([selected_candidate, ratio, x_0, cut_me + x_0])

            # lets plot
            if plot:
                plt.figure()
                plot_signals(selected_candidate, label="SEGMENTED")
        else:
            pass

    return X

















