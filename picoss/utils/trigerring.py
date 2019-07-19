import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import obspy
from obspy.signal.trigger import trigger_onset, recursive_sta_lta
from tqdm import tqdm

from knowaves_utils import save_pickle, load_pickle

############################################
# PARAMETERS - typically taken from the bash file.
############################################

# Folders with all the data and stuff
datafolder = "data_paper"
dest_folder = "parametros_silvio"

# Datasets selection. We shall pass to "cluster mode"
datasets = ["YC"]
stations = ['BELO', 'BESA', 'BERG']

# frequency filters and stuff.
bandpass = [2, 12]
filtering = True

# type of trigger
trigger_type = "recstalta"
nsta = 2
nlta = 15

# trigger on/off
trig_on = 2.5
trig_off = 1.0


def plot_results(tracename, data, cft, on_of, trig_on, trig_off):
    ax = plt.subplot(211)
    plt.title(tracename)
    plt.plot(data, 'k')
    ymin, ymax = ax.get_ylim()
    plt.vlines(on_of[:, 0], ymin, ymax, color='r', linewidth=2)
    # plt.vlines(on_of[:, 1], ymin, ymax, color='b', linewidth=2)
    plt.subplot(212, sharex=ax)
    plt.plot(cft, 'k')
    plt.hlines([trig_on, trig_off], 0, len(cft), color=['r', 'b'], linestyle='--')
    plt.axis('tight')
    plt.show()


def save_stalta(destination_folder, filename, data, cft, on_of, trig_on, trig_of, fm):
    dict_toSave = {'filename': filename,
                   'data': data,
                   'cft': cft,
                   'on_of': on_of,
                   'trig_on': trig_on,
                   'trig_of': trig_of,
                   'fm': fm
                   }

    save_pickle(destination_folder, filename, dict_toSave)


# I should change this in a futute
def load_stalta(folder, filename, plot=False):
    dict_loaded = load_pickle(os.path.join(folder, filename))
    return dict_loaded


def plot_from_stalta(folder, filename):
    dict_loaded = load_pickle(os.path.join(folder, filename))
    plot_results(dict_loaded['filename'], dict_loaded['data'], dict_loaded['cft'], dict_loaded['on_of'],
                 dict_loaded['trig_on'], dict_loaded['trig_of'])
    print "... Loaded %s " % (filename)


def merge_numpy(stream):
    data = []
    for k in xrange(len(stream)):
        data.append(stream[k].data)
    return np.asarray(np.hstack(data))


def make_trigger(origin_folder, filename, dest_folder, trig_on, trig_of, trigger_type, nsta, nlta, plot=True):
    stream = obspy.read(os.path.join(origin_folder, filename))

    freqmin = bandpass[1]
    freqmax = bandpass[0]
    print freqmin, freqmax
    filtered = stream.filter("bandpass", freqmin=bandpass[1], freqmax=bandpass[0])
    fm = float(filtered[0].stats.sampling_rate)
    to_process = filtered.copy()
    merged = to_process.merge(method=0)

    if np.isnan(merged).any():
        to_process = filtered.copy()
        data = merge_numpy(to_process)
        cft = recursive_sta_lta(data, int(nsta * fm), int(nlta * fm))
        on_of = trigger_onset(cft, trig_on, trig_off)

    else:
        # we can process the whole day.
        data = merged[0]
        cft = recursive_sta_lta(data, int(nsta * fm), int(nlta * fm))
        on_of = trigger_onset(cft, trig_on, trig_off)

    # we can process the whole day.
    cft = recursive_sta_lta(data, int(nsta * fm), int(nlta * fm))
    on_of = trigger_onset(cft, trig_on, trig_of)

    if plot:
        plot_results(filename, data, cft, on_of, trig_on, trig_of)

    save_stalta(dest_folder, filename, data, cft, on_of, trig_on, trig_of, fm)


def process_data(origin_folder, dest_folder, trig_on, trig_of, trigger_type, nsta, nlta):
    if not os.path.isdir(dest_folder):
        os.mkdir(dest_folder)

    """
    print "... Processing the data from %s " % (origin_folder)
    print "... Storing data at %s " % (dest_folder)
    print "Trigger type %s " % (trigger_type)
    print "nsta %s " % (nsta)
    print "nlta %s " % (nlta)

    print "Trigger on: %s " % (trig_on)
    print "Trigger off %s " % (trig_of)
    """

    print "Bandpass - freqs: %s " % (bandpass)

    # we iterate over all the folder and process all the data
    for k in tqdm(os.listdir(origin_folder)):
        make_trigger(origin_folder, k, dest_folder, trig_on, trig_of, trigger_type, nsta, nlta, plot=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='origin folder', required=False)
    parser.add_argument('-d', help='destination folder', required=False)
    parser.add_argument('-f', help='(Optional) seismic fle trace', required=False)
    parser.add_argument('-l', '--list', nargs='+', help='<Required> STA/LTA params', required=True)

    args = parser.parse_args()

    origin_folder = sys.argv[2]
    dest_folder = sys.argv[4]
    sta_lta_params = sys.argv[6:]

    trig_on = float(sta_lta_params[0])
    trig_off = float(sta_lta_params[1])
    nsta = int(sta_lta_params[2])
    nlta = int(sta_lta_params[3])
    trigger_type = str(sta_lta_params[4])

    bandpass = [float(sta_lta_params[5]), float(sta_lta_params[6])]

    process_data(origin_folder, dest_folder, trig_on, trig_off, trigger_type, nsta, nlta)
