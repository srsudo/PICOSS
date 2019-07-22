import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import obspy
from scipy import io
from six.moves import cPickle


class Converter():

    def __init__(self):
        self.formats = ['npy', 'mat', 'save']

    def convert_2_mat(self, filestream, seg_file, destination_file, chop):

        if self.check_extensions([seg_file, destination_file]):

            try:
                # st = obspy,read(filestream)
                data = self.load_pickle(seg_file)
                if int(chop) == 1:
                    self.do_chop(filestream, data, destination_file)
                else:
                    self.save_mat(data, destination_file)

            except (IOError, OSError) as e:
                print "Segmentation file not found!"

        else:
            print "Only %s formats are supported. Please, check the input command!" % \
                  (self.formats)

    def check_extensions(self, files):
        return all([True if x.split(".")[-1] in self.formats else False for x in files])

    def check_if_exists(self, folders):
        return all([True if os._exists(x) else False for x in folders])

    def load_pickle(self, filename):
        try:
            f = open(filename, 'rb')
            loaded_obj = cPickle.load(f)
            f.close()
            return loaded_obj
        except (IOError, OSError) as e:
            print "File not found!"

    def read_mat(self, filename):
        """Returns a serialized object from a pickle file. """
        return io.loadmat(filename)

    def save_mat(self, obj, destination_file):
        """Serialize an object into matlab format."""
        io.savemat(destination_file, mdict={'arr': obj})

    def plot(self, to_plot, fm):
        time_Vector = np.linspace(0, to_plot.shape[0] / fm, num=to_plot.shape[0])
        plt.plot(time_Vector, to_plot)
        plt.show()

    def do_chop(self, filestream, data, destination_file):
        try:
            final_data = []
            st = obspy.read(filestream)
            # I will assume the signal is extracted raw - and then people can apply their filtering a
            # at the processing stage.
            trace_loaded = st.merge(method=0)
            trace_loaded = trace_loaded._cleanup()
            trace = trace_loaded[0]

            fm = trace.stats.sampling_rate
            signal = trace.data

            if fm == 75.19:
                fm = 75.0

            final_data.append((filestream, data[0]))
            print "Storing the signals: "
            for k in data[1:]:
                start_time = int(float(k[0]) * fm)
                end_time = int(float(k[1]) * fm)
                # print float(k[0]), float(k[1])
                chunk = np.asarray(signal[start_time:end_time])
                # self.plot(chunk, fm) #uncomment to see the signals
                final_data.append((k, chunk))

            # add pickle_save
            # add mat save
            self.save_mat(final_data, destination_file)

        except (IOError, OSError) as e:
            print "Trace not found. Please, check the input!"


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--stream", required=True, help="Filename (with folders) of the main Stream.")
    ap.add_argument("-d", "--data", required=True, help="The .npy file containing the segmentation")
    ap.add_argument("-o", "--output", required=True, help="Filename (.mat) to store the data for MATLAB")
    ap.add_argument("-c", "--chop", required=False, help="IF we want to chop the signals or not")
    args = vars(ap.parse_args())

    stream_filename = args['stream']
    npy_file = args['data']
    destination_file = args['output']
    chop = args['chop']
    converter = Converter()
    converter.convert_2_mat(stream_filename, npy_file, destination_file, chop)
