# Given values
sqm = 2500  # Area in square meters
depth = 2    # Depth in meters
h = 80       # Height in meters
g = 9.81     # Acceleration due to gravity in m/s^2

# Mass of water
m = sqm * depth * 1000  # Volume in cubic meters, assuming 1000 kg/m^3 density for water

# Potential energy in joules
E = m * g * h

# Convert energy to megawatt-hours (MWh)
E_MWh = E / (3.6e9)  # 1 MWh = 3.6e9 J

E, E_MWh

print(f"Energy is {E_MWh} MWh")