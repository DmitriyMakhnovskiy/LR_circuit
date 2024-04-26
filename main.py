#
# Calculating all parameters of the LR circuit, including impedance, total current, power and power factor, and
# compensation capacitor for its series or parallel connection.
#
# Dr. Dmitriy Makhnovskiy, City College Plymouth, England, 09.04.2024
#

import math

# Given values
R = 80  # Resistance (in ohms)
L = 8e-2  # Inductance (in henries)
f = 100  # Frequency (in Hz)

omega = 2.0 * f * math.pi  # Angular frequency (in rad/s)

# Calculate impedance
Z = complex(R, omega * L)

# Calculate impedance magnitude
Z_magnitude = abs(Z)

# Calculate current in the circuit
V = 220  # Voltage (in volts)
I = V / Z_magnitude

# Calculate RMS current
I_rms = I / math.sqrt(2)

# Calculate phase angle (in radians)
phi_rad = math.atan(-omega * L / R)

# Convert phase angle to degrees
phi_deg = math.degrees(phi_rad)

# Calculate power factor
power_factor = math.cos(phi_rad)

# Calculate power consumed by the circuit
P = I_rms ** 2 * R

# Calculate the compensation capacitance for the series connection
C1 = 1 / (omega ** 2 * L)
C1 = C1 / 1.0e-6  # uF

# Calculate the compensation capacitance for the parallel connection
C2 = L / (R ** 2 + L ** 2 * omega ** 2)
C2 = C2 / 1.0e-6  # uF

# Print results
print('')
print("Circuit Impedance (Z): {:.3f} + {:.3f}j ohms".format(Z.real, Z.imag))
print("|Z| (Impedance Magnitude): {:.3f} ohms".format(Z_magnitude))
print("Current in the circuit (I): {:.3f} A".format(I))
print("RMS Current (I_rms): {:.3f} A".format(I_rms))
print("Phase Angle (φ): {:.2f} degrees".format(phi_deg))
print("Power Factor (cosφ): {:.2f}".format(power_factor))
print("Power Consumed by the Circuit (P): {:.2f} W".format(P))
print("Compensation Capacitance for the series connection: {:.3f} uF".format(C1))
print("Compensation Capacitance for the parallel connection: {:.3f} uF".format(C2))

