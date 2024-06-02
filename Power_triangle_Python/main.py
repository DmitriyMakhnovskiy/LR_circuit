
# Calculating the vector sum of powers and the power factor

import math  # math library

sign = lambda num: 1 if num > 0 else -1 if num < 0 else 0  # sign function
pi = math.pi  # pi = 3.14159...

# Loads' parameters
pf_array = [1.0, -0.707, 0.9]  # power factor array for the three loads ("+" for leading, and "-" for lagging)
PW_array = [30.0, 150.0, 60.0]  # true power array (kW) for the three loads

# Parameters for LTspice simulations
V0 = 220.0  # voltage amplitude in V(t) = V0sin(w*t)
f = 50  # frequency in Hz

# Calculations of the powers, phase, and power factor
ind = [i for i in range(len(pf_array))]  # indexes
PVA_array = [pw / abs(pf) for pw, pf in zip(PW_array, pf_array)]  # VA or kVA
PVAR_array = [sign(pf) * (pav**2 - pw**2)**0.5 for pav, pw, pf in zip(PVA_array, PW_array, pf_array)]  # VAR or kVAR
print('\n'.join([f'PVA{i + 1} = ({round(pw, 3)}, {round(pvar, 3)})' for pw, pvar, i in zip(PW_array, PVAR_array, ind)]))
PW = sum([pw for pw in PW_array])  # true power of the whole circuit
PVAR = sum([pvar for pvar in PVAR_array])  # reactive power of the whole circuit
PVA = (PW**2 + PVAR**2)**0.5  # apparent power of the whole circuit
phase_rad = math.atan2(PVAR, PW)  # phase (rad) of the total current in the circuit
phase_deg = phase_rad * 180.0 / pi  # phase (degree) of the total current in the circuit
PF = math.cos(phase_rad)  # power factor of the whole circuit
print('')
print('True power of the whole circuit = ', round(PW,3), ' kW')
print('Reactive power of the whole circuit = ', round(PVAR,3), ' kVAR')
print('Apparent power of the whole circuit = ', round(PVA,3), ' kVA')

print('')
if sign(phase_rad) < -0.0005:
    print('Power factor of the whole circuit = ', round(PF,3), ' (lagging)')
elif sign(phase_rad) > 0.0005:
    print('Power factor of the whole circuit = ', round(PF, 3), ' (leading)')
else:
    print('Power factor of the whole circuit = ', 1, ' (perfect matching)')

print('Phase (rad) of the total current in the circuit = ', round(phase_rad,3))
print('Phase (deg) of the total current in the circuit = ', round(phase_deg,3))

# Calculation of the equivalent circuit parameters
print('')
print('Equivalent circuit parameters:')
PW_array = [x * 1.0e+3 for x in PW_array]  # transfer kW to W for calculations
Vrms = V0 / (2.0**0.5)  # voltage rms amplitude
w = 2.0 * pi * f
Irms_array = [pw / (abs(pf) * Vrms) for pw, pf in zip(PW_array, pf_array)]  # currents in the loads A
print('')
print('\n'.join([f'Current_{i + 1} = {round(Irms * 2.0**0.5, 3)} A' for Irms, i in zip(Irms_array, ind)]))

print('')
R_array = [pw / (Irms**2) for pw, Irms in zip(PW_array, Irms_array)]  # resistances
print('\n'.join([f'Resistance_{i + 1} = {R} Ohms' for R, i in zip(R_array, ind)]))
X_array = [(Vrms**2 / (Irms**2) - R**2)**0.5 for Irms, R in zip(Irms_array, R_array)]  # reactances

for i in range(len(pf_array)):
    if pf_array[i] < -0.0:
        L = X_array[i] / w
        print(f'Component_{i + 1} = {L} H')
    elif 0.0 < pf_array[i] < 1.0:
        C = 1.0 / (X_array[i] * w)
        print(f'Component_{i + 1} = {C} F')
    else:
        print(f'Component_{i + 1} = no reactive part')