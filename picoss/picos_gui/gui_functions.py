# -*- coding: utf-8 -*-

"""
This script includes generic functionalities for the main interface
"""
import sys
sys.path.append('..')

from PyQt4 import QtGui, QtCore
import webbrowser
import numpy as np
from scipy import io
from utils import picos_utils


def msg_box(msg1, msg2):
    """
    Python function to create messages and informative for the users
    Parameters
    ----------
    msg1 : str
        The text (body) message
    msg2 : str
        The informative message
    Returns
        True when the users click the ok
    -------
    """

    msgBox = QtGui.QMessageBox()
    msgBox.setIcon(QtGui.QMessageBox.Information)
    msgBox.setText(msg1)
    msgBox.setInformativeText(msg2)
    msgBox.addButton(QtGui.QMessageBox.Ok)
    ret = msgBox.exec_()
    if ret == QtGui.QMessageBox.Ok:
        return True


def check_digits(number):
    """
    Function that check the input canvas to see if is a number or not
    Args:
        number: str
            The number we want to check
    Returns:
    bool
        True if success, False otherwise
    """
    if number.replace('.', '', 1).isdigit():
        return True
    elif number.isdigit():
        return True
    else:
        return False


def check_emptiness(param):
    """
    Function that checks a canvas to see if is empty or not
    Args:
        param : str
        The string we want to check if is empty or not
    Returns:
    Bool
        True if empty, False if not.
    """
    if param not in ['\n', '\r\n']:
        return True
    else:
        return False


def load_picking_dictionary(filename):
    pass


def web_info(browser_path):
    """
    Function that given a browser path, opens a related information webpage about it.
    Args:
        browser_path: str:
            The browserpath we would like to open
    """
    webbrowser.open(browser_path)


def save_segmentation_table(destination_folder, filename, data_format, segmentation_table):
    """
    FIle that given the destination folder, the filename, the data format and the segmentation table,
    it checks the extension and save it in a folder.
    Args:
        destination_folder : str
            The destination folder where we want to save the file
        filename : str
            The filename where we would like to save it
        data_format : str
            The type of data format (.npy, .mat or .save) that we would like to save the data
        segmentation_table : dict
            A dict containing the segmentation table from our results

    Returns:
    Bool
        True if saved properly, false otherwise.
    """

    file_toSave = "%s%s%s" % (destination_folder, filename, data_format)

    try:
        if data_format == ".npy":
            np.save(file_toSave, segmentation_table)
        elif data_format == ".p":
            picos_utils.save_pickle(destination_folder, filename+data_format, segmentation_table)
        else:
            """Serialize an object into matlab format."""
            io.savemat(file_toSave, mdict={'arr': segmentation_table})

    except IOError as e:

        print(e.errno)
