# How to use PICOSS

Once we execute the command:

After docker-compose is running, PICOSS main window will appear. If your are running from Conda environment, you may need to run ```sh python run_picos.py``` first.

Main trace of interest can be loaded from data centers or local repositories. For more information about how to load data from data centers, please refer to the [Wiki](https://github.com/srsudo/picos_development/wiki).

Loaded data will appear on the main window upper part. All signals are high-pass filtered with 0.5 Hz corner frequency by default. By mouse-clicking and dragging on the signal,
a rectangle can be draw. For all data signals contained inside the current rectangle, spectrograms and FFTs can be visualized.

![alt main_window](https://github.com/srsudo/picos_development/blob/master/info/img/picos-main.png)

Zoom and span options can be accessed in the Zoom/Span menu. We recommend to use the keyboard shortcuts:

  - CTRL + Z : Zoom on/off
  - CTRL + S : Span option (can drag the graph in any direction)
  - CTRL + U : Undone and restore original view.

Once a label is selected, we can submit the current window by clicking "Submit Current Window". When finished, all information can be stored by clicking "Submit all Trace".

## Modifying trace parameters

Imagine you want to change the high-pass corner frequency or band-pass the signal. These options are available at "Data/Frequency and Filtering" options. Make sure any of the radio
buttons are checked, otherwise the program will not modify the main trace.

## Visualize other components

PICOSS allow to visualize other components from the current trace. You can do so by looking at: "Extra_info" menu.

  - "Visualize other components": Visualize other component *at the current selected rectangle*. If the rectangle changes, re-plot is needed.
 
## Visualize other stations

PICOSS allow to visualize other stations as well. You can do that by clicking at "Visualize other stations". It allows you to plot the trace from another station of your choice. 

You will notice that there is an extra orange line. **It represents the alignment of this station with respect the main one**. In other words, if the main station starts at 00:00:09, and the 
second station started at 00:00:19, there will be a -10 seconds that is represented by this extra orange line. This should help to visualize when the seismic signals arrived.

Similar interactivity is provided. Keyboards: ZOOM (Z), SPAN (S), Undo (U) and Quit (Q) options can be accessed. 

## I want my analysis back..how can I do that?

About how to retrieve the signals/segmentation files is explained [here](https://github.com/srsudo/picos_development/blob/master/info/tutorials/data_conversion.md)  

## Notes

  *Make sure before running docker-compose run, data is stored at "./data" folder !*
  