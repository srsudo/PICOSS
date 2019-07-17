# Data management 

One of the main features of PICOSS is to collect all the data for posterior analysis. In the folder "utils/", a set of
tools and scripts are provided for data management, store and analysis. 

## How to convert the data to ".mat" files:

To just convert the data from ".save" to ".mat", if we open the script "conversion.sh" (with a text editor for example), 
we will see something like this. 

```
folder_stream="data/1997/BGA/SBZ.D/MV.MBGA..SBZ.D.1997.176" #the folder where the main trace is located
folder_segmented="segmented_data/MV_MBGA_SBZ_D_1997_176_86387.save" #the folder with the segmentation file of interest
mat_tosave="MV_MBGA_SBZ_D_1997_176_86387.mat" #the name we want to save the results-
chop=0 #0 just convert just the output file from ".save", to ".mat", without storing the signals
```

In the above example, the file *MV_MBGA_SBZ_D_1997_176_86387.save* is converted in *MV_MBGA_SBZ_D_1997_176_86387.mat*. 
Notice we should specify the paths for both files. The variable "chop" is "0" as we are just converting from ".save" 
to ".mat". The final file is named as *MV_MBGA_SBZ_D_1997_176_86387.mat*.

For your specific files, **folders and filename need to be specified by you**

Once you have done that, just run: 

```
bash conversion.sh
```

And you will get your file ready for MATLAB.

*Warning: This convert only the segmentation results from PICOSS (start, end, label, PeakAmp, Duration, Q, Comments).
 You may still need the main trace for further processing.* 

## How to collect the data from ".save" files

If we want to convert from ".save" to ".mat" file **and store the signals**, this is the option to go. The file "conversion.sh"
should look like this: 


```
folder_stream="data/1997/BGA/SBZ.D/MV.MBGA..SBZ.D.1997.176" #the folder where the main trace is located
folder_segmented="segmented_data/MV_MBGA_SBZ_D_1997_176_86387.save" #the folder with the segmentation file of interest
mat_tosave="MV_MBGA_SBZ_D_1997_176_86387.mat" #the name we want to save the results-
chop=1 
```

With `chop=1`, meaning it will get the segmented signals and store it along with all the information we need. Then, 
run: 

```
bash conversion.sh
```