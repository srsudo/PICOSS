#!/usr/bin/env bash

# 2018 University of Liverpool (Author: Angel Bueno)
#
# This script do sta_lta of your choice, from a single seismic file or from a given folder with seismic traces.
# If used from a folder, this script process ALL SEISMIC TRACES at once. Use it only IF AND ONLY IF you already
# know the STA /LTA hyperparameters. Otherwise, we would recommend to use the STA/LTA with PICOSS GUI, in a seismic traces
# of your choice. Once you are happy with the obtained results, you can use this script to process the whole data.


# data and network configuration parameters
# In picos examples, default data is in "data/1997/BGA/SBZ.D

data_main="data" #the folder where we have all the data.
networkcode="YC" #the volcano network code - use this if data is organized as in the format year/network_code/station/channel
year='2007' #the year we want to process.
station='BELO' #the station we want to process
channel='HHZ.D' # the channel

DATA_folder="${data_main}/${year}/${networkcode}/${station}/${channel}"
DEST_folder="stalta_${networkcode}_${year}_${station}_${channel}"

#Filtering OPTIONS.
up_freq=12 #we will assume bandpass
low_freq=2

######### STALTA parameters

#type of trigger
trigger_type="recstalta"
nsta=2
nlta=15

#trigger on/off
trig_on=2.5
trig_off=1.0

echo ============================================================================
echo "                           STA/LTA PIPELINE                               "
echo ============================================================================

echo "Reading from: ${DATA_folder}"
echo "Storing on: ${DEST_folder}"

echo "Params: trigger_type: ${trigger_type},
              nsta: ${nsta},
              nlta: ${nlta},
              trigger_on: ${trig_on},
              trigger_off: ${trig_off}"


#we call the method
python utils/trigerring.py -o $DATA_folder -d $DEST_folder -l $trig_on $trig_off $nsta $nlta $trigger_type $up_freq $low_freq
















