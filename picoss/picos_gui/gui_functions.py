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


def web_info(browserpath):
    """
    Function that given a browser path, opens a related information webpage about it.
    Args:
        browserpath: str:
            The browserpath we would like to open
    """
    webbrowser.open(browserpath)
