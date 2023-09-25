import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_context("paper")
sns.set_theme(style="darkgrid", palette="bright")

rho = 1000
g = 9.8065
visc = 10**(-6)
wet_sur = 1.107
lwl = 2377
Cb = 0.656
Beam = 0.387
mean_draught = 0.126

x_axis = np.array([0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])


def froude(speed, lwl, g):
    return speed / (np.sqrt(g*lwl))


def reynold(speed, lwl, visc):
    return (speed * lwl) / visc


def sink_angle(sink, lwl):
    return np.arctan(sink/lwl)


def sink(angle, lwl):
    return np.tan(angle)*lwl


def trim(AP_angle, FP_angle):
    return AP_angle - FP_angle


def tot_resistance_coeff(speed, rtm, rho, wet_sur):
    return rtm / (0.5 * rho * (speed**2) * wet_sur)


def frict_resistance_coeff(Re):
    return 0.075 / (np.log10(Re) - 2)**2


def residual_coeff(C_t, C_f, k):
    return C_t - (1 + k)*C_f


# Velocity data
speed = np.array([0.60275, 0.70217, 0.80365, 0.90250,
                 1.00364, 1.10407, 1.20450, 1.30490, 1.40453])
# Standard deviaton of velocity
std_speed = np.array([0.01124, 0.01179, 0.01342, 0.01354,
                     0.01525, 0.01619, 0.01737, 0.01679, 0.01283])

# Sink in FP data
sinkFP = np.array([4.98362, 6.19303, 7.11419, 8.11837,
                  10.11390, 11.47583, 13.17266, 16.76340, 17.93348])
# Standard deviation of sink in FP
std_sinkFP = np.array([0.76550, 0.60052, 0.3370, 0.93073,
                      1.25116, 1.75432, 1.09393, 1.8391, 2.06895])

# Sink in AP data
sinkAP = np.array([5.51017, 6.43280, 7.06091, 7.61554,
                  8.94634, 9.49537, 10.58371, 13.62703, 15.96010])
# Standard deviation of sink in AP
std_sinkAP = np.array([0.81769, 0.78061, 0.67071, 0.90143,
                      0.90815, 1.23164, 0.92941, 1.20382, 1.74544])

# See the project report for trim calculation -----
FP_len = lwl/2 - 215
AP_len = lwl/2 - 396

mean_trim = np.rad2deg(
    trim(sink_angle(sinkAP, AP_len), sink_angle(sinkFP, FP_len)))
worst_trim_AP = np.rad2deg(
    trim(sink_angle(sinkAP+std_sinkAP, AP_len), sink_angle(sinkFP-std_sinkFP, FP_len)))
worst_trim_FP = np.rad2deg(
    trim(sink_angle(sinkAP-std_sinkAP, AP_len), sink_angle(sinkFP+std_sinkFP, FP_len)))
least_sink = np.rad2deg(
    trim(sink_angle(sinkAP-std_sinkAP, AP_len), sink_angle(sinkFP-std_sinkFP, FP_len)))
most_sink = np.rad2deg(
    trim(sink_angle(sinkAP+std_sinkAP, AP_len), sink_angle(sinkFP+std_sinkFP, FP_len)))
# -----

# Towing resistance data
rtm = np.array([1.0801, 1.52449, 1.98786, 2.42580,
                3.08479, 3.88261, 4.90852, 6.98475, 10.49765])
# Standard deviation of towing resistance
std_rtm = np.array([0.0091, 0.83624, 0.95623, 1.08389,
                    1.10720, 1.53109, 1.92933, 2.00474, 1.77734])

# Froude number from the experiment
Fn = froude(speed, lwl/1000, g)

# Reynolds number from the experiment
Re = reynold(speed, lwl/1000, visc)

# Total resistance coefficient og the mean towing resistance
Ct = tot_resistance_coeff(speed, rtm, rho, wet_sur)

# Frictional resistance
Cf = frict_resistance_coeff(Re)

# φ and k from the form factor equation
phi = (Cb/(lwl/1000)) * np.sqrt(Beam *
                                (2*mean_draught + (sinkAP + sinkFP)/1000))

k = 0.6*phi + 145*(phi**(3.5))

# Residual resistance
Cr = residual_coeff(Ct, Cf, k)

# The Froude Numbers corresponding to the Holtrop and Hollenbach calculated values.
Fn_app = [0.172, 0.185, 0.197, 0.209, 0.221, 0.234,
          0.246, 0.258, 0.271, 0.283, 0.295, 0.308]
Holtrop = [.000115, .000186, .000283, .000407, .000564, .000745,
           .000937, .001169, .00149, .001886, .002261, .002515]
Hollenbach = [.000829, .000873, .000938, .001025, .001133,
              .001262, .001413, .001585, .001845, .002169, .002551, .002999]

# Plotting everything after one another
for plot in range(4, 5):
    
    # Total resistance force plot with standard deviation
    if plot == 0:
        plt.plot(x_axis, rtm, 'o', linestyle='dashed', color='firebrick',
                 label='Mean Total Resistance Force')
        plt.fill_between(x_axis, rtm - std_rtm, rtm + std_rtm,
                         color='mediumaquamarine', alpha=0.2)
        plt.vlines(x_axis, rtm-std_rtm, rtm+std_rtm,
                   label="Standard Deviation of Mean", color='teal')
        plt.ylabel("Resistance Force [N]")
        plt.xlabel("Velocity [m/s]")
        plt.legend(loc=2)
        plt.show()

    # Speed plot with standard deviation
    if plot == 1:
        plt.plot(x_axis, speed, 'o', linestyle='dashed', color='firebrick',
                 label='Mean Measured Velocity')
        plt.fill_between(x_axis, speed - std_speed, speed + std_speed,
                         color='mediumaquamarine', alpha=0.2)
        plt.vlines(x_axis, speed-std_speed, speed+std_speed,
                   label="Standard Deviation of Mean", color='teal')
        plt.ylabel("Measured Velocity [m/s]")
        plt.xlabel("Velocity Setpoint [m/s]")
        plt.legend(loc=2)
        plt.show()

    # Trim plots, see report. 
    if plot == 2:
        plt.plot(x_axis, worst_trim_AP, 'o', linestyle='solid', color='violet',
                 label='Biggest Possible Trim at AP.                                       |  + std(AP), - std(FP)')
        plt.plot(x_axis, worst_trim_FP, 'o', linestyle='solid', color='purple',
                 label='Biggest Possible Trim at FP.                                       |  - std(AP), + std(FP)')
        plt.plot(x_axis, least_sink, 'o', linestyle='solid', color='blue',
                 label='Trim at Minimum Possible Sink on both AP and FP.   |  - std(AP), - std(FP)')
        plt.plot(x_axis, most_sink, 'o', linestyle='solid', color='limegreen',
                 label='Trim at Maximum Possible Sink on both AP and FP.  |  + std(AP), + std(FP)')
        plt.plot(x_axis, mean_trim, 'o', linestyle='solid', color='red',
                 label='Mean Trim')
        plt.ylabel("Trim Angle [deg]")
        plt.xlabel("Velocity [m/s]")
        plt.legend(
            loc=2)
        plt.title(
            "When the trim is positive, it means that the vessel's AP is more inside the water than the FP")
        plt.show()

    # Plot of the mean sink in AP and FP and the standard deviation of both
    if plot == 3:
        plt.plot(x_axis, sink(sink_angle(sinkFP, FP_len), lwl/2), 'o', linestyle='None', color='blue',
                 label='Mean sinkFP')
        plt.plot(x_axis, sink(sink_angle(sinkAP, AP_len), lwl/2), 'o', linestyle='None', color='red',
                 label='Mean sinkAP')
        plt.plot(x_axis, sink(sink_angle(sinkAP, AP_len), lwl/2)+sink(sink_angle(std_sinkAP, AP_len), lwl/2), '--',
                 linestyle=(0, (1, 10)), color='tomato')
        plt.plot(x_axis, sink(sink_angle(sinkAP, AP_len), lwl/2)-sink(sink_angle(std_sinkAP, AP_len), lwl/2), '--',
                 linestyle=(0, (5, 10)), color='tomato')
        plt.plot(x_axis, sink(sink_angle(sinkFP, FP_len), lwl/2)+sink(sink_angle(std_sinkFP, FP_len), lwl/2), '--',
                 linestyle=(0, (1, 10)), color='lightskyblue')
        plt.plot(x_axis, sink(sink_angle(sinkFP, FP_len), lwl/2)-sink(sink_angle(std_sinkFP, FP_len), lwl/2), '--',
                 linestyle=(0, (5, 10)), color='lightskyblue')
        plt.fill_between(x_axis, sink(sink_angle(sinkAP, AP_len), lwl/2) - sink(sink_angle(std_sinkAP, AP_len), lwl/2), sink(sink_angle(sinkAP, AP_len), lwl/2) + sink(sink_angle(std_sinkAP, AP_len), lwl/2),
                         color='lightcoral', alpha=0.2)
        plt.fill_between(x_axis, sink(sink_angle(sinkFP, FP_len), lwl/2)-sink(sink_angle(std_sinkFP, FP_len), lwl/2), sink(sink_angle(sinkFP, FP_len), lwl/2)+sink(sink_angle(std_sinkFP, FP_len), lwl/2),
                         color='paleturquoise', alpha=0.2)
        plt.ylabel("Sink [mm]")
        plt.xlabel("Velocity [m/s]")
        plt.legend(loc=2)
        plt.show()

    # Plot of the residual resistance in comparison with the Hollenbach and Holltrop method
    if plot == 4:
        plt.plot(Fn, Cr, 'D', linestyle='solid', color='firebrick',
                 label='Experimental')
        plt.plot(Fn_app, Holtrop, 'o', linestyle='solid', color='dodgerblue',
                 label='Holtrop')
        plt.plot(Fn_app, Hollenbach, 'o', linestyle='solid', color='limegreen',
                 label='Hollenbach')
        plt.ylabel("Residual Resistance Coefficient [-]")
        plt.xlabel("Froude Number [m/s]")
        plt.title(
            "Comparison of experimental results against the Holtrop- and Hollenbach method")
        plt.legend(loc=2)
        plt.show()

# Data calculated for the runs at 6 m/s, used for error calculation in the report
x_axis_6 = ['6_1', '6_2', '6_3', '6_4', '6_5']
sinkAP_6 = np.array([5.72469, 6.23697, 5.20692, 5.54426, 5.83802])
sinkFP_6 = np.array([4.94483, 5.63175, 4.32591, 4.98441, 5.03118])

std_sinkAP_6 = np.array([0.64753, 0.94929, 0.76620, 0.97098, 0.75447])
std_sinkFP_6 = np.array([0.75868, 0.80189, 0.79974, 0.70404, 0.76313])

real_sink_AP = sink(sink_angle(std_sinkAP_6, AP_len), lwl/2)
real_sink_FP = sink(sink_angle(std_sinkFP_6, FP_len), lwl/2)
