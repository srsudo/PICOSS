# STA/LTA at scale

PICOSS allows you to process seismic data at scale with STA/LTA, for posterior analysis. In the folder "utils/", the
script `trigerring.py` allows you to use the data from any given data folder. THis can be done by using the bash script 
`make_sta_lta.sh`

## How to use the bash script:

We will run the script with the test data of Montserrat volcano (MV). In picos examples, default data is in `data/1997/BGA/SBZ.D`. 
Taking the data contained in that folder, and open `make_sta_lta.sh` in your favourite text editor (like vim).

```
data_main="data" #the folder where we have all the data.
networkcode="MV" #the volcano network code - use this if data is organized as in the format year/network_code/station/channel
year='1997' #the year we want to process.
station='BGA' #the station we want to process
channel='SBZ.D' # the channel

DATA_folder="${data_main}/${year}/${networkcode}/${station}/${channel}"
DEST_folder="stalta_${networkcode}_${year}_${station}_${channel}"

```

In the above example, STA/LTA is applied to all the files inside the folder *data/1997/BGA/SBZ.D* and results are stored in
*stalta_MV_1997_BGA_SBZ.D*. Notice we should specify the paths for origin and destination files,
**CHANGE THIS ACCORDING TO YOUR OWN DATA FOLDER STRUCTURE**. 

Once you have done that, we need to adjust the STA/LTA parameters (a good tutorial can be found [here] (https://goo.gl/aKxjSk)):

```
#Filtering OPTIONS.
up_freq=12 #we will assume bandpass
low_freq=2

######### STALTA parameters

#type of trigger
trigger_type="recstalta"
nsta=5
nlta=10

#trigger on/off
trig_on=1.2
trig_off=0.5
```

When parameters are defined, we just need to run the bash script from a terminal. Run: 

```
bash make_sta_lta.sh
```
The destination folder will be created and sta/lta results will be stored inside. 