import numpy as np
import math
import csv
from scipy.integrate import simpson
from genPowerPulse import genPowerCurve

def main():
    pw = np.linspace(10E-3, 150E-3, num=70)
    edep = np.linspace(50, 200, num=75)
    V = math.pi * 0.1 * (4.096E-3)**2  # Ensure volume calculation is correct
    dens = 10431.5

    #sweep_all(pw, edep, V, dens)
    check_transient("transient.csv", V, dens)

def check_transient(csvFn, V, dens):
    time = []
    volPwr = []
    with open(csvFn, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            t,p = map(float, row)
            time.append(t)
            volPwr.append(p)
    
    time = np.array(time)
    volPwr = np.array(volPwr)
    pw = find_fwhm(time, volPwr)

    # Integrate signal (W/m³) to get energy (J/m³)
    integral_energy_j_per_m3 = integrate_signal(time, volPwr)

    # Convert energy from J/m³ to cal/m³
    joules_to_calories = 1 / 4.184
    integral_energy_cal_per_m3 = integral_energy_j_per_m3 * joules_to_calories

    integral_energy_cal_per_g = integral_energy_cal_per_m3 / (dens * 1000)

    # Return the results
    print(f"Integral Energy (J/m³): {integral_energy_j_per_m3}")
    print(f"Integral Energy (cal/m³): {integral_energy_cal_per_m3}")
    print(f"Integral Energy (cal/g): {integral_energy_cal_per_g}")
    print(f"Pulse Width (s): {pw}")    

def sweep_all(pwList, edepList, V, dens):
    # Conversion factor from Joules to calories (1 cal = 4.184 J)
    joules_to_calories = 1 / 4.184

    for width in pw:
        for dep in edep:
            powerTuple = genPowerCurve(dep, width, V, dens, 250)

            time_unzip, pwr_unzip = zip(*powerTuple)
            pw_calc = find_fwhm(time_unzip, pwr_unzip)

            # Integrate signal (W/m³) to get energy (J/m³)
            integral_energy_j_per_m3 = integrate_signal(time_unzip, pwr_unzip)

            # Convert energy from J/m³ to cal/m³
            integral_energy_cal_per_m3 = integral_energy_j_per_m3 * joules_to_calories

            # Convert energy from cal/m³ to cal/g
            integral_energy_cal_per_g = integral_energy_cal_per_m3 / (dens * 1000)  # dens in kg/m³, so dens * 1000 gives g/m³

            ed_calc = integral_energy_cal_per_g

            pw_error = width - pw_calc
            edep_error = dep - ed_calc

            # Debugging output
            print(f"pw (Expected, Calc, Error): {width},{pw_calc},{pw_error} --- edep: {dep},{ed_calc},{edep_error}")
            #print(f"  Integral Energy (J/m³): {integral_energy_j_per_m3}")
            #print(f"  Integral Energy (cal/m³): {integral_energy_cal_per_m3}")
            #print(f"  Integral Energy (cal/g): {integral_energy_cal_per_g}")

def integrate_signal(time, signal):
    # Using Simpson's rule for numerical integration
    integral = simpson(signal, x=time)
    return integral

def find_fwhm(time, signal):
    # Find the peak value and its index
    peak_value = np.max(signal)
    peak_index = np.argmax(signal)

    # Find the half-maximum value
    half_max_value = peak_value / 2

    # Find the indices where the time series crosses the half-maximum value
    left_index = np.where(signal[:peak_index] <= half_max_value)[0][-1]
    right_index = np.where(signal[peak_index:] <= half_max_value)[0][0] + peak_index

    # Interpolate to find the exact crossing points
    left_time = np.interp(half_max_value, [signal[left_index], signal[left_index + 1]],
                          [time[left_index], time[left_index + 1]])
    right_time = np.interp(half_max_value, [signal[right_index - 1], signal[right_index]],
                           [time[right_index - 1], time[right_index]])

    # Calculate FWHM
    fwhm = right_time - left_time

    return fwhm

if __name__ == "__main__":
    main()

