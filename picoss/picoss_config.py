#!/usr/bin/env python

"""
Main configuration File for PICOSS extra functionalities, and default destination folders.
Folder configuration may be different across setups. Make sure it is adjusted accordingly.
"""
import os

webpage_project = "https://github.com/srsudo/picos/tree/master"
info = os.path.join(webpage_project, "info", "howto")
about = os.path.join(webpage_project, "info", "about.ipynb")
seismology = os.path.join(webpage_project, "info", "seismology")


# Default folder to save the segmented data
destination_folder = "segmented_data"
if os.path.isdir(destination_folder):
    pass
else:
    os.mkdir(destination_folder)


# Signal processing parameters
nfft = 600
highpass = 0.5  # High-pass filter by-default for background noise and ease visualization
