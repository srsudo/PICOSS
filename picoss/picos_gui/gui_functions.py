# -*- coding: utf-8 -*-

"""
This script includes generic functionalities for the main interface
"""

from PyQt4 import QtGui
import webbrowser


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

    msgBox = QtGui.QMessageBox(self)
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
