from apread import APReader
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np
import seaborn as sns
sns.set_context("paper")
sns.set_theme(style="darkgrid", palette="bright")

# [Sensor] [Sensor name]
# 0        Time  1 - default sample rate                                                                                                                                                               
# 1        Rtm
# 2        SinkFP
# 3        SinkAP
# 4        WP_Wash
# 5        UL_WaterLevel
# 6        Position
# 7        Speed
# 8        Waterlevel_Calc

sensors = [1,2,3,4,7]

# Reading in the data of the different runs
readers = [APReader('bin/run0.6_1.BIN'), APReader('bin/run0.6_2.BIN'), APReader('bin/run0.6_3.BIN'), APReader('bin/run0.6_4.BIN'), APReader('bin/run0.6_5.BIN')
           , APReader('bin/run0.7_1.BIN'), APReader('bin/run0.8_1.BIN'), APReader('bin/run0.9_1.BIN'), APReader('bin/run1.0_1.BIN'), APReader('bin/run1.1_1.BIN')
           , APReader('bin/run1.2_1.BIN'), APReader('bin/run1.3_1.BIN'), APReader('bin/run1.4_1.BIN')]

reader = [APReader('bin/run0.6_1.BIN')]

# The ranges are the indices of the data that is used for calculation of the statistical variables. These are hand selected and chosen when the signal was steady.
ranges_speed = [[24640, 28985], [5170, 9800], [5520, 9675], [5205, 9540], [5145, 9335], [4800, 8300]
          , [5685, 8300], [5860, 8280], [5150, 7565], [6250, 8090], [5370, 6900], [5330, 6800], [5370, 6560]]

ranges_rtm = [[24640, 28985], [5745, 9605], [5520, 9675], [5205, 9715], [5145, 9785], [4610, 8610]
          , [5540, 8610], [5930, 8500], [5980, 7800], [6600, 8300], [5740, 7180], [5580, 6950], [5815, 6755]]

ranges_sink = [[24640, 28985], [5300, 9800], [5520, 9675], [4760, 9900], [5145, 9335], [4400, 8300]
          , [5330, 8540], [5700, 8650], [5150, 8020], [6120, 8090], [5370, 7340], [5330, 7000], [5370, 7030]]

# This range is only used for visualization, and not calculation
ranges_wave = [[23200, 30000]]

# The list of ranges
ranges = [0,ranges_rtm, ranges_sink, ranges_sink,ranges_wave, 0, 0, ranges_speed]


# Variable to keep track of which range one should use. 
run_number = 0

# Function to filter the noise from the signal. The value of 50 is visually chosen, such that the noise is gone and the data is intact. 
# This is a source of error. The value is constant this whole project.
def gauss_filter(data, sigma=50):
  gauss_filtered_signal = ndimage.gaussian_filter1d(data,sigma)
  return gauss_filtered_signal

# Iterating through the runs
for run in reader:
  for sensor in sensors:
    sample_period = run.Channels[0].data.max()   # Using the end time of the run to select the period. (Channel[0] is time, check the top of the code file)
    samples = run.Channels[0].length             # Using the time-channel to find out how many entries of data we have. 
    sample_fq = samples / sample_period          # Calculating the sample frequency of the run.

    x_axis = np.linspace(0,samples,samples)     # The x-axis will represent the number of sample points. to find the time, one could divide with the sample frequency.
    data = run.Channels[sensor].data             # The sensor variable, initialized on the top of the code file, selects the channel and gives the data. This code is for the Speed.
    name = run.Channels[sensor].Name             # The name for use in the plot
    f1 = gauss_filter(data)                       # Returns the filtered data

    start_sample = ranges[sensor][run_number][0] # Selecting the starting and ending index for the data   
    end_sample = ranges[sensor][run_number][1]   # Selecting the ending index for the data

    start_time = start_sample/sample_fq          # Calculating the start time of the range
    end_time = end_sample/sample_fq              # Calculating the end time of the range

    window = data[start_sample:end_sample]       # Selecting the window to preform the statistical analysis

    mean = window.mean()                         # Calculating the mean of the window
    std = window.std()                           # Calculating the standard deviation of the window
    var = window.var()                           # Calculating the variance of the window
    time_elapsed = round(end_time-start_time, 3) # Calculating the time elapsed during the window

    # ----- Plotting the data -----
    
    # Units for the plotting
    units = [0,'Total Resistance Force [N]', 'SinkFP [m]', 'SinkAP [m]', 'Wave Elevation [m]', 0, 0, 'Velocity [m/s]']

    if (sensor == 2 or sensor == 3): # For sinkFP/AP I show the data in mm, therefore the if check for those two sensors
      title = name+" "+run.fileName+' Mean: '+str(round(mean*1000,5))+'mm Std: '+str(round(std*1000,5))+'mm Var: '+str(round(var*1000,5))+'mm, Time Elapsed: '+str(time_elapsed)
    else:
      title = name+" "+run.fileName+' Mean: '+str(round(mean,5))+' Std: '+str(round(std,5))+' Var: '+str(round(var,5))+', Time Elapsed: '+str(time_elapsed)

    # Unfiltered data, whole time-series
    plt.plot(x_axis[int(np.round(start_sample*0.75, 0)):int(np.round(end_sample*1.25, 0))]/sample_fq, data[int(np.round(start_sample*0.75, 0)):int(np.round(end_sample*1.25, 0))], color='lightblue', label="Unfiltered Signal")
    # Filtered data, whole time-series
    plt.plot(x_axis[int(np.round(start_sample*0.75, 0)):int(np.round(end_sample*1.25, 0))]/sample_fq, f1[int(np.round(start_sample*0.75, 0)):int(np.round(end_sample*1.25, 0))], color='steelblue', label="Filtered Signal")

    # The red lines visualize the window of calculation in the plot
    plt.axvline(start_sample/sample_fq, linestyle=(0, (5, 5)), color='red', label="Steady window for calculation")
    plt.axvline(end_sample/sample_fq, linestyle=(0, (5, 5)), color='red')
    
    # Assigning the correct unit on the y-axis
    plt.ylabel(units[sensor])

    plt.xlabel('Time [s]')
    # plt.title(title)
    plt.legend()

    # Showing the whole time-series
    plt.show()

    # Unfiltered data in the window of calculation
    plt.plot(x_axis[start_sample:end_sample]/sample_fq, data[start_sample:end_sample], color='lightblue', label="Unfiltered Signal")

    # Unfiltered data in the window of calculation
    plt.plot(x_axis[start_sample:end_sample]/sample_fq, f1[start_sample:end_sample], color='steelblue', label="Filtered Signal")

    # Plotting the std-lines
    plt.axhline((mean+std), linestyle=(0, (5, 5)), color='darkslategray', label=('Standard Deviation = ±' + str(np.round(std, 5))))
    plt.axhline((mean-std), linestyle=(0, (5, 5)), color='darkslategray')

    # Plotting the mean
    plt.axhline((mean), linestyle='solid', color='red', label=('Mean ' + name + ' = ' + str(np.round(mean, 5))))

    # Assigning the correct unit on the y-axis
    plt.ylabel(units[sensor])

    plt.xlabel('Time [s]')
    # plt.title(title)
    plt.legend()
    plt.show()
  
    

  # Increasing the run number for the next iteration
  run_number += 1